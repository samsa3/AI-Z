# 02 — Legal research

Every material decision must point to a **concrete, verifiable source** (article number + link).

## Where the detailed analysis lives
| Branch | File | Covers |
|---|---|---|
| GDPR | [`legal/gdpr.md`](legal/gdpr.md) | A. Scope · B. Principles · C. Legal basis · D. Special categories · E. Automated decisions · F. Privacy by design · G. External model & transfers · H. DPIA, transparency, records |
| EU AI Act | [`legal/ai-act.md`](legal/ai-act.md) | Roles, high-risk (Annex III), prohibited emotion recognition, human oversight, deployer duties, explanation, timeline |
| EDPB guidelines | [`legal/edpb-guidelines.md`](legal/edpb-guidelines.md) | Art. 22 / WP251 (meaningful human review) · Pseudonymisation 01/2025 |
| National & sector | [`legal/national-and-sector.md`](legal/national-and-sector.md) | GDPR Art. 88, UAVG / BDSG, sector rules — _TODO_ |

## What is at stake
AI agents can save teams hours (e.g. reading 40 applications and comparing them with job criteria). But every prompt sent to an external model like OpenAI is a **transfer of personal data** to a processor, often outside the EU. Without controls, a company would send names, contact details and sometimes health or other sensitive data to a third party, with no legal basis and no way to prove compliance.

1. **GDPR** — only strictly necessary data (Art. 5); sensitive data prohibited by default (Art. 9); no rejection by a machine alone (Art. 22).
2. **EU AI Act** — AI that filters or evaluates job candidates is **high-risk** (Annex III): human oversight (Art. 14), informing candidates and workers (Art. 26), explanations (Art. 86). Emotion recognition at work is banned (Art. 5). High-risk duties are deferred to Dec 2027 (to verify), not cancelled.
3. **Accountability** — the company must *demonstrate* compliance (Art. 5(2)), not just claim it.

## Answers to the 7 challenge questions
| # | Question | Answer | Sources | Detail |
|---|---|---|---|---|
| Q1 | Which legal requirements apply? | GDPR (any info on an identifiable person; pseudonymised data still counts); AI Act (recruiting = high-risk); EDPB guidelines; national law (Art. 88) | GDPR Art. 2, 4(1), Rec. 26; AI Act Art. 6, Annex III | all branches |
| Q2 | Which data may the agent process? | Only with an Art. 6 basis per data category, and only what is necessary; no Art. 9/10 data | GDPR Art. 5(1)(c), 6, 9, 10 | gdpr.md B–D |
| Q3 | What may OpenAI receive? | Only task-relevant data, pseudonymised; OpenAI = processor with DPA; transfer safeguards outside EU | GDPR Art. 5(1)(c), 28, 44–46 | gdpr.md G |
| Q4 | What must be removed / pseudonymised / local? | Names → pseudonymise; contact details → remove; indirect identifiers → generalise; special categories → block; re-identification key → local only | GDPR Art. 4(5), 9, 25, 32(1)(a), Rec. 26–29; EDPB 01/2025 | gdpr.md F, edpb |
| Q5 | Which steps are not permitted? | Art. 9/10 data to the model; solely automated decisions; emotion inference at work; reuse for another purpose | GDPR Art. 5(1)(b), 9, 10, 22; AI Act Art. 5(1)(f) | gdpr.md D–E, ai-act |
| Q6 | Which decisions must humans control? | The final decision — with **meaningful** review (authority, competence, sees original data), ability to override and stop | GDPR Art. 22, Rec. 71; AI Act Art. 14, 26(2); WP251 | gdpr.md E, ai-act, edpb |
| Q7 | How are rules enforced technically? | BRANE policies (ALLOW / PROTECT / LOCAL ONLY / BLOCK), fail-closed, logs, 5 security tests | GDPR Art. 25, 32(1)(d), 5(2) | policy matrix, test protocol |

## Open points
- [ ] **Choose our use case** (current analysis follows the recruiting example — the jury wants our own)
- [ ] Pick **one Art. 6 basis per data category** (6(1)(b) usual for applications; 6(1)(f) needs balancing + Art. 21)
- [ ] Verify Digital Omnibus dates (Reg. 2026/1744) in the Official Journal
- [ ] Verify WP251 wording; check if EDPB 01/2025 was finalised
- [ ] National law (UAVG) and sector rules
