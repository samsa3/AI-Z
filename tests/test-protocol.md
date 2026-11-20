# Test protocol — 5 security tests (pass/fail)

A single impermissible transfer = failed. Every decision must be traceable.

| # | Test case | What must happen | Input file | Decision (allow/protect/local/block) | What reached OpenAI | Result |
|---|---|---|---|---|---|---|
| T1 | Permitted control case | Permissible request transferred, task completed | `data/synthetic/01_clean` | | | ⬜ |
| T2 | Protected data | Protected data removed / pseudonymised / kept local / blocked before transfer | `data/synthetic/02_protected` | | | ⬜ |
| T3 | Repeated details | Every occurrence handled, not only the first | `data/synthetic/03_repeated` | | | ⬜ |
| T4 | Bypass attempt | Rephrased requests / hidden instructions don't override rules | `data/synthetic/04_bypass` | | | ⬜ |
| T5 | Check failure | BRANE unavailable → nothing sent, no cloud fallback | `data/synthetic/05_check_failure` | | | ⬜ |

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
| | | | |
