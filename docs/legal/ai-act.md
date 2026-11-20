# EU AI Act — Regulation (EU) 2024/1689

Source: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024R1689 (original text; amended by the Digital Omnibus, Regulation (EU) 2026/1744 — see timeline, **to verify**).
Overview: [`../02-legal-research.md`](../02-legal-research.md).

## Roles (Art. 3(3), 3(4))
- *Provider* = develops an AI system and places it on the market under its own name → **our team** (we build the agent).
- *Deployer* = uses an AI system "under its authority" → the company / HR department using it.
- OpenAI = provider of the general-purpose model.

## Is a recruiting agent high-risk? (Art. 6(2), 6(3), Annex III point 4)
- Annex III 4(a): AI "intended to be used for the recruitment or selection of natural persons, in particular … to analyse and filter job applications, and to evaluate candidates" → **high-risk**.
- Annex III 4(b): promotion, termination, task allocation, monitoring/evaluating workers → also high-risk.
- Art. 6(3) exception: not high-risk if no material influence on the decision, e.g. "(a) a narrow procedural task" or "(d) a preparatory task to an assessment". **But** "an AI system referred to in Annex III shall **always** be considered to be high-risk where the AI system performs **profiling** of natural persons."
- Art. 6(4): a provider relying on the exception must **document** it and register (Art. 49(2)).
- → Comparing candidates with job criteria = profiling (GDPR Art. 4(4)) → **treat the agent as high-risk**; don't rely on the "preparatory task" exception.

## Prohibited practice to avoid (Art. 5(1)(f))
AI inferring **emotions** "in the areas of workplace and education institutions" is banned (except medical/safety). → BLOCK any feature analysing tone, video or "personality" from interviews or cover letters.

## Human oversight (Art. 14)
Humans must be able to: (a) understand capacities and limitations and monitor operation; (b) stay aware of **automation bias**; (c) correctly interpret the output; (d) decide "not to use … or to otherwise disregard, override or reverse the output"; (e) interrupt the system ("stop" button).
→ Technical rules: **recommendation with reasons**, never a final verdict; HR can override; kill-switch; UI warns against blind reliance.

## Deployer obligations (Art. 26) — governance & business case
- 26(1) use per instructions for use
- 26(2) human oversight by people with "the necessary competence, training and authority"
- 26(7) employers inform **workers' representatives and affected workers** before use
- 26(9) use provider info to carry out the **GDPR Art. 35 DPIA**
- 26(11) inform people that they are subject to a high-risk AI system (→ candidates must be told)

## AI literacy (Art. 4)
Providers and deployers ensure "a sufficient level of AI literacy of their staff" → short training for HR users.

## Bias and data (Art. 10(5))
Special categories may **exceptionally** be processed only where "strictly necessary" for **bias detection and correction**, with safeguards. → In the agent, keep Art. 9 data BLOCKED; run bias tests separately on synthetic data.

## Right to explanation (Art. 86)
A person affected by a decision based on an Annex III system can obtain "clear and meaningful explanations of the role of the AI system in the decision-making procedure and the main elements of the decision". Complements GDPR Art. 22 + Recital 71. → Log which criteria the agent matched for each candidate.

## Timeline — important for the jury
| Obligation | Original date (Art. 113) | After Digital Omnibus (Reg. 2026/1744)* |
|---|---|---|
| Prohibitions (Art. 5) + AI literacy (Art. 4) | 2 Feb 2025 | unchanged — **already apply** |
| Transparency (Art. 50) | 2 Aug 2026 | unchanged — **already applies** |
| Annex III high-risk (recruiting) | 2 Aug 2026 | **2 Dec 2027** |
| Annex I high-risk (products) | 2 Aug 2027 | 2 Aug 2028 |

*Based on secondary sources; **verify against the Official Journal** text of Reg. 2026/1744 before quoting. Pitch argument: high-risk duties are **deferred, not cancelled** → building them now = compliance by design.

## Sources
- AI Act original text: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024R1689
- Digital Omnibus timeline (secondary): https://www.globalsuitesolutions.com/digital-omnibus-ai-regulation-2026-1744/ · https://www.aiacto.eu/en/blog/digital-omnibus-ai-act-report-2027 · https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-omnibus-vii-deadline-delay-20260/
