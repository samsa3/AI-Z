# 01 — Use case

## Business process
_What task does the agent automate or simplify? For whom?_

## Input data
| Data | Example (synthetic) | Personal data? (GDPR Art. 4(1)) | Special category? (Art. 9 / 10) |
|---|---|---|---|
| | | | |

## Agent output
_What the agent produces._

## Human in the loop
_Which decisions stay with a human, and who?_ (GDPR Art. 22)

## Why it's legally demanding
_GDPR / AI Act / sector rules that make this hard._

## GDPR qualification checklist
Source: GDPR — https://eur-lex.europa.eu/eli/reg/2016/679/oj

- [ ] **Controller / processor** — who is the controller (our client company)? OpenAI = processor? (Art. 4(7)–(8), Art. 28)
- [ ] **Data subjects** — whose data is processed? (applicants, patients, customers, employees…)
- [ ] **Purpose** — one clearly defined purpose (Art. 5(1)(b))
- [ ] **Legal basis** — which point of Art. 6(1)? Why?
- [ ] **Special categories** present in the input? (Art. 9) → if yes, which exception, or block them
- [ ] **Criminal data** present? (Art. 10)
- [ ] **Automated decision** with legal/significant effect? (Art. 22) → keep the decision human
- [ ] **DPIA needed?** (Art. 35(3): systematic automated evaluation, large-scale special categories)
- [ ] **Transfer outside the EU?** (Art. 44–46)

## AI Act qualification checklist
Source: [`legal/ai-act.md`](legal/ai-act.md)
- [ ] Our role = provider; client = deployer (Art. 3(3)-(4))
- [ ] Is the use case in **Annex III** (employment, credit, education…)? → high-risk
- [ ] Does it **profile** people? → always high-risk (Art. 6(3))
- [ ] Any **prohibited practice** (e.g. emotion recognition at work, Art. 5(1)(f))?

> Note: our legal analysis currently follows the **recruiting** example of the challenge. Confirm it or replace it with our own use case.
