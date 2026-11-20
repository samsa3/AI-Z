"""Local policy layer: detect, classify and protect sensitive content BEFORE
anything is handed to the BRANE gateway (defence in depth).

BRANE remains the mandatory control point for every model request. This layer
exists so that (a) our rules are enforced even if a BRANE policy is
misconfigured and (b) every decision is logged on our side for the test
protocol. Rule IDs (R2, R3, ...) match docs/03-policy-matrix.md.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

POLICY_FILE = Path(__file__).resolve().parent.parent / "policies.json"

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
URL_RE = re.compile(r"\b(?:https?://|www\.)\S+|\b(?:linkedin|github|xing)\.com/\S+", re.I)
PHONE_RE = re.compile(r"(?<![\w])(?:\+|00)?\d[\d \-/().]{7,}\d(?![\w])")
IBAN_RE = re.compile(r"\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){2,7}(?: ?[A-Z0-9]{1,4})?\b")
LABELLED_ID_RE = re.compile(
    r"\b(?:BSN|SSN|national id(?:entity)?(?: number| no\.?)?|passport(?: number| no\.?)?|"
    r"tax id|id number|social security(?: number)?)\s*[:#]?\s*[A-Z0-9][A-Z0-9 \-]{4,}",
    re.I,
)
ADDRESS_LINE_RE = re.compile(r"^(?:address|home address|street)\s*:.*$", re.I | re.M)
NAME_FIELD_RE = re.compile(
    r"^(?i:name|full name|applicant|candidate|from|signed|regards|kind regards|sincerely)\s*[:,]?\s*"
    r"([A-Z][a-z'\-]+(?: [A-Z][a-z'\-]+){1,2})\s*$",
    re.M,
)
HONORIFIC_RE = re.compile(r"\b(?:Mr|Ms|Mrs|Mx|Dr)\.? ([A-Z][a-z'\-]+)")
# Split on sentence ends, but not after initials / titles ("M. Fictus", "Dr. X").
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])(?<!\b[A-Z]\.)(?<!\bM[rsx]\.)(?<!\bMrs\.)(?<!\bDr\.)\s+|\n+")


@dataclass
class Event:
    rule: str
    measure: str
    category: str
    count: int


@dataclass
class SanitiseResult:
    text: str
    events: list[Event] = field(default_factory=list)
    mapping: dict[str, str] = field(default_factory=dict)  # pseudonym -> real name (LOCAL ONLY)
    removed_values: list[str] = field(default_factory=list)  # kept in memory only, for the egress check

    def add(self, rule: str, policy: dict, count: int) -> None:
        if count:
            r = policy["rules"][rule]
            self.events.append(Event(rule, r["measure"], r["category"], count))


def load_policy(path: Path = POLICY_FILE) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _lexicon_re(terms: list[str]) -> re.Pattern:
    return re.compile(r"\b(?:" + "|".join(re.escape(t) for t in terms) + r")", re.I)


def _name_variants(full_name: str) -> list[str]:
    parts = full_name.split()
    first, last = parts[0], parts[-1]
    variants = {
        full_name,
        f"{last}, {first}",
        f"{first[0]}. {last}",
        f"{first[0]}.{last}",
        last,
        first,
    }
    for title in ("Mr", "Ms", "Mrs", "Mx", "Dr"):
        variants.add(f"{title}. {last}")
        variants.add(f"{title} {last}")
    return sorted(variants, key=len, reverse=True)  # longest first


def find_names(text: str, known_names: list[str] | None = None) -> list[str]:
    names = list(dict.fromkeys(known_names or []))
    for m in NAME_FIELD_RE.finditer(text):
        if m.group(1) not in names:
            names.append(m.group(1))
    return names


def sanitise(text: str, policy: dict | None = None, known_names: list[str] | None = None) -> SanitiseResult:
    """Apply every local rule to `text` and return the protected version."""
    policy = policy or load_policy()
    res = SanitiseResult(text=text)
    lex = policy["lexicons"]

    # --- Segment rules first (R9 injection, R6 special category, R7 criminal) ---
    segment_rules = [
        ("R9", _lexicon_re(lex["embedded_instruction"]), "[REMOVED: embedded instruction]"),
        ("R6", _lexicon_re(lex["special_category"]), "[REMOVED: special-category data]"),
        ("R7", _lexicon_re(lex["criminal_record"]), "[REMOVED: criminal-record data]"),
    ]
    sentences = SENTENCE_SPLIT_RE.split(res.text)
    counts = {rule: 0 for rule, _, _ in segment_rules}
    kept = []
    for s in sentences:
        replaced = None
        for rule, rx, marker in segment_rules:
            if rx.search(s):
                counts[rule] += 1
                res.removed_values.append(s)
                replaced = marker
                break
        kept.append(replaced if replaced else s)
    res.text = "\n".join(k for k in kept if k.strip())
    for rule in counts:
        res.add(rule, policy, counts[rule])

    # --- R5: ID and financial numbers ---
    n = 0
    for rx in (LABELLED_ID_RE, IBAN_RE):
        res.removed_values += rx.findall(res.text)
        res.text, k = rx.subn("[REMOVED: id/financial number]", res.text)
        n += k
    res.add("R5", policy, n)

    # --- R3: contact details (every occurrence) ---
    n = 0
    for rx, marker in ((EMAIL_RE, "[REMOVED: email]"), (URL_RE, "[REMOVED: url]"),
                       (ADDRESS_LINE_RE, "[REMOVED: address]"), (PHONE_RE, "[REMOVED: phone]")):
        res.removed_values += rx.findall(res.text)
        res.text, k = rx.subn(marker, res.text)
        n += k
    res.add("R3", policy, n)

    # --- R2: names -> stable pseudonym at every occurrence and variant ---
    names = find_names(text, known_names)
    n = 0
    prefix = policy.get("pseudonym_prefix", "PERSON")
    for i, name in enumerate(names, start=1):
        token = f"{prefix}_{i:02d}"
        res.mapping[token] = name
        for variant in _name_variants(name):
            rx = re.compile(r"(?<![\w])" + re.escape(variant) + r"(?![\w])")
            res.text, k = rx.subn(token, res.text)
            n += k
    # Honorific + surname we were not told about -> still pseudonymise.
    for m in list(HONORIFIC_RE.finditer(res.text)):
        if not m.group(1).startswith(prefix):
            token = f"{prefix}_{len(res.mapping) + 1:02d}"
            res.mapping[token] = m.group(0)
            res.text, k = re.subn(re.escape(m.group(0)), token, res.text)
            n += k
    res.add("R2", policy, n)
    return res


def egress_violations(payload: str, res: SanitiseResult, policy: dict | None = None) -> list[str]:
    """Final check on the exact outbound payload. Any hit => BLOCK the request."""
    policy = policy or load_policy()
    lex = policy["lexicons"]
    problems = []
    if EMAIL_RE.search(payload):
        problems.append("email")
    if IBAN_RE.search(payload) or LABELLED_ID_RE.search(payload):
        problems.append("id/financial number")
    if PHONE_RE.search(payload):
        problems.append("phone")
    for cat in ("special_category", "criminal_record"):
        if _lexicon_re(lex[cat]).search(payload):
            problems.append(cat)
    for name in res.mapping.values():
        for v in _name_variants(name):
            if len(v) > 2 and re.search(r"(?<![\w])" + re.escape(v) + r"(?![\w])", payload):
                problems.append("name")
                break
    return sorted(set(problems))
