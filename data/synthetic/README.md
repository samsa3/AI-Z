# Synthetic data

**Only synthetic data.** No real personal or confidential company data, ever.

Prepare at least one file per test case:

| File | Purpose |
|---|---|
| `01_clean.*` | Permitted control case — only task-relevant data |
| `02_protected.*` | Sensitive data hidden in the middle of the text |
| `03_repeated.*` | Same name/contact details appearing several times |
| `04_bypass.*` | Hidden instruction / rephrased request trying to override the rules |
| `05_check_failure.*` | Normal input, run with BRANE disabled |
