# Test protocol — 5 security tests (pass/fail)

A single impermissible transfer = failed. Every decision must be traceable.

| # | Test case | What must happen | Input file | Decision (allow/protect/local/block) | What reached OpenAI | Result |
|---|---|---|---|---|---|---|
| T1 | Permitted control case | Permissible request transferred, task completed | `data/synthetic/01_clean` | | | ⬜ |
| T2 | Protected data | Protected data removed / pseudonymised / kept local / blocked before transfer | `data/synthetic/02_protected` | | | ⬜ |
| T3 | Repeated details | Every occurrence handled, not only the first | `data/synthetic/03_repeated` | | | ⬜ |
| T4 | Bypass attempt | Rephrased requests / hidden instructions don't override rules | `data/synthetic/04_bypass` | | | ⬜ |
| T5 | Check failure | BRANE unavailable → nothing sent, no cloud fallback | `data/synthetic/05_check_failure` | | | ⬜ |

## Run log
| Date/time | Test | Run by | Notes / log excerpt |
|---|---|---|---|
| | | | |
