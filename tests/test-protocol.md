# Test protocol — 5 security tests (pass/fail)

A single impermissible transfer = failed. Every decision must be traceable.

| # | Test case | What must happen | Input file | Decision (allow/protect/local/block) | What reached OpenAI | Result |
|---|---|---|---|---|---|---|
| T1 | Permitted control case | Permissible request transferred, task completed | `data/synthetic/01_clean` | ALLOW | sanitised CV text + criteria | PASS (mock) |
| T2 | Protected data | Protected data removed / pseudonymised / kept local / blocked before transfer | `data/synthetic/02_protected` | PROTECT (R2,R3) + BLOCK segments (R5,R6) | `PERSON_01`, no contact/ID/health data | PASS (mock) |
| T3 | Repeated details | Every occurrence handled, not only the first | `data/synthetic/03_repeated` | PROTECT (R2 ×8, R3 ×4) | only `PERSON_01`, every variant replaced | PASS (mock) |
| T4 | Bypass attempt | Rephrased requests / hidden instructions don't override rules | `data/synthetic/04_bypass` | BLOCK segments (R9 ×3) + PROTECT (R2,R3) | no injection text, no PII | PASS (mock) |
| T5 | Check failure | BRANE unavailable → nothing sent, no cloud fallback | `data/synthetic/05_check_failure` | BLOCK (R10) | nothing (unreachable / HTTP 500 / not configured) | PASS (mock) |

## Legal requirement behind each test
Details: [`../docs/02-legal-research.md`](../docs/02-legal-research.md)

| Test | Policy rules | Legal anchor |
|---|---|---|
| T1 Permitted control case | R1 | GDPR Art. 6 (legal basis) + 5(1)(c) — the agent still does its job |
| T2 Protected data | R2–R8 | GDPR Art. 9, 10, 5(1)(c), 25 |
| T3 Repeated details | R2, R3 | GDPR Art. 25(2), 32 — measures effective at every occurrence |
| T4 Bypass attempt | R9 | GDPR Art. 5(1)(f), 32(1)(b) |
| T5 Check failure | R10 | GDPR Art. 32(1)(b)(d), 5(2) accountability |
| All | R13 | GDPR Art. 5(2), 32(1)(d) regular testing; AI Act Art. 86 explanation |

## Run log
| Date/time | Test | Run by | Notes / log excerpt |
|---|---|---|---|
| 2026-11-20 15:20 UTC | T1–T5 (+T5b HTTP 500, T5c not configured, no-direct-OpenAI check) | @rodrigo-claude | `python -m unittest discover -s tests/security -t .` → 8/8 OK against **local mock gateway** (`agent/brane_agent/mock_brane.py`), which records every request it receives. Real BRANE not yet tested. |
| 2026-11-20 ~16:00 UTC | T1–T4 **live**, T5 live (invalid key → 401) + unreachable | @rodrigo-claude | Live BRANE, model `openrouter:anthropic/claude-haiku-5.5`, workbench policy still **fully open**. T1 ALLOW, T2–T4 PROTECT by our local layer; BRANE headers on all: `action=allow, pii-detected=false, redacted=false, routed-to=cloud` (nothing sensitive left for BRANE to see). T5: 401 and unreachable → BLOCK, no model answer used. BRANE's own enforcement not yet tested (policy not configured). |
