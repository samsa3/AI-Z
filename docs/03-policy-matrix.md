# 03 — Policy matrix

Measures: **ALLOW** (transfer OK) · **PROTECT** (pseudonymise / mask / remove) · **LOCAL ONLY** (never leaves local env) · **BLOCK** (no processing/transfer)

> Generic rules based on GDPR, AI Act and EDPB (see [`02-legal-research.md`](02-legal-research.md)). Examples follow the recruiting case — adapt to our use case and fill the Art. 6 basis per category.

| # | Data category | Example (synthetic) | Measure | Technical rule in BRANE | Art. 6 basis | Legal justification | Implemented? | Tested in |
|---|---|---|---|---|---|---|---|---|
| R1 | Task-relevant content | qualifications, experience | **ALLOW** (after basis check) | Forward to OpenAI | 6(1)(b) or (f) | GDPR Art. 5(1)(b)-(c), 6 | ✅ prototype — passes through after local rules | T1 |
| R2 | Direct identifiers | "Lisa Becker" | **PROTECT** — pseudonymise | Stable token (`CANDIDATE_01`) at **every** occurrence | | GDPR Art. 4(5), 5(1)(c), 25(1), 32(1)(a), Rec. 26/28 | ✅ `policy.py` names→`PERSON_nn`, all variants | T2, T3 |
| R3 | Contact details | email, phone, address | **PROTECT** — remove | Delete before transfer | | GDPR Art. 5(1)(c), 25(2) | ✅ `policy.py` email/phone/url/address | T2, T3 |
| R4 | Indirect identifiers | rare job title, employer, exact dates | **PROTECT** — generalise | e.g. "large retailer", year only | | GDPR Rec. 26; EDPB Guidelines 01/2025 | ⬜ not yet | T2 |
| R5 | ID & financial numbers | national ID, IBAN | **BLOCK** | Remove / block request | none needed for task | GDPR Art. 5(1)(c), 5(1)(f), 32, 87 | ✅ `policy.py` IBAN + labelled IDs | T2 |
| R6 | Special categories | health, religion, ethnicity | **BLOCK** | Never sent to external model | — | GDPR Art. 9(1), 22(4) | ✅ `policy.py` sentence removed (keyword lexicon) | T2 |
| R7 | Criminal records | convictions | **BLOCK** | Never sent | — | GDPR Art. 10 | ✅ `policy.py` sentence removed (keyword lexicon) | T2 |
| R8 | Re-identification key | `CANDIDATE_01` ↔ person | **LOCAL ONLY** | Stored locally, named authorised staff, git-ignored | | GDPR Art. 4(5), 32, Rec. 29; EDPB 01/2025 | ✅ `mappings/<run>_mapping.json`, git-ignored | T2, T3 |
| R9 | Instructions embedded in documents | "ignore previous rules…" | **BLOCK** override | Treated as data, policies always applied | | GDPR Art. 5(1)(f), 32(1)(b) | ✅ `policy.py` sentence removed + hardened system prompt | T4 |
| R10 | BRANE unavailable | — | **BLOCK** (fail-closed) | No direct / fallback call to OpenAI | | GDPR Art. 5(1)(f), 25, 32(1)(b)(d) | ✅ `gateway.py` any error → BLOCK, no fallback | T5 |
| R11 | Emotion / personality inference | tone of cover letter, video | **BLOCK** (feature not built) | — | — | AI Act Art. 5(1)(f) | n/a — feature not built; prompt forbids inference | — |
| R12 | Final decision | hire / reject | **Human only** | Recommendation with reasons; human can override / stop | | GDPR Art. 22(1)(3), Rec. 71; AI Act Art. 14, 26(2); WP251 | ✅ output = recommendation + human-review notice | — |
| R13 | Decision logs | policy, timestamp, criteria matched | **LOCAL ONLY** | Pseudonyms only, no raw personal data | | GDPR Art. 5(2), 30; AI Act Art. 86 | ✅ `logs/audit.jsonl`, pseudonyms only, git-ignored | all |

Minimum required: **3 justified and implemented rules** — R2, R6 and R10 are the strongest for the demo.

> Implementation status refers to the local policy layer on branch `agent/policy-engine-prototype` (Python, tested against a **mock** BRANE gateway). Enforcement by the real BRANE gateway is **not yet verified**.
