# GDPR — detailed analysis

Source: Regulation (EU) 2016/679 (GDPR), official English text — https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679
Text in "quotes" is verbatim from the GDPR; the rest is a summary. Overview and answers: [`../02-legal-research.md`](../02-legal-research.md).

```
GDPR for an AI agent behind BRANE
├── A. Scope & definitions ............ Is it personal data? Who is responsible?
├── B. Principles (Art. 5) ............ Minimisation, purpose limitation → drives PROTECT rules
├── C. Legal basis (Art. 6) ........... Is the processing allowed at all? → ALLOW condition
├── D. Special categories (Art. 9) .... Health, ethnicity, religion... → BLOCK / LOCAL ONLY
├── E. Automated decisions (Art. 22) .. Human-in-the-loop → "no autonomous decision"
├── F. Privacy by design (Art. 25, 32)  Pseudonymisation as a technical measure → PROTECT
├── G. External AI model provider ..... Processor (Art. 28) + transfers (Art. 44–46)
└── H. Risk & accountability .......... DPIA (Art. 35), transparency (Art. 13), records (Art. 30)
```

---

## A. Scope & definitions (Art. 4, Recital 26)

| Term | Key meaning (Art. 4) | Why it matters for the agent |
|---|---|---|
| Personal data (4(1)) | Any info relating to an identified or identifiable natural person — name, ID number, location data, online identifier, or physical/genetic/mental/economic/cultural/social identity factors | Names, emails, phone numbers, addresses, and indirect identifiers in free text all count |
| Processing (4(2)) | Any operation on personal data, incl. "disclosure by transmission" | Sending a prompt to OpenAI **is** processing |
| Profiling (4(4)) | Automated evaluation of personal aspects, e.g. "performance at work, economic situation, health, … reliability, behaviour" | Scoring/ranking people = profiling → see E |
| Pseudonymisation (4(5)) | Data can no longer be attributed to a person "without the use of additional information", kept separately and protected | What BRANE does with `CANDIDATE_01`; the mapping table stays in the protected environment |
| Controller (4(7)) / Processor (4(8)) | Controller decides purposes and means; processor acts on its behalf | Company = controller; OpenAI = processor → G |
| Consent (4(11)) | "freely given, specific, informed and unambiguous" | Weak basis in employer/employee settings (power imbalance) |
| Data concerning health (4(15)) | Physical or mental health data, incl. health-care info | Triggers Art. 9 → D |

**Recital 26:** pseudonymised data that can be re-linked with additional information **is still personal data**. Only truly anonymous data falls outside the GDPR. → Pseudonymisation reduces risk (Recital 28) but does **not** remove GDPR obligations.

---

## B. Principles (Art. 5) → source of the PROTECT rules

| Principle | Art. | Technical rule |
|---|---|---|
| Lawfulness, fairness, transparency | 5(1)(a) | Legal basis (C) + inform data subjects (H) |
| Purpose limitation | 5(1)(b) | Data collected for X not reused for Y → agent restricted to one task |
| **Data minimisation** | 5(1)(c) | "adequate, relevant and limited to what is necessary" → strip every field the model doesn't need |
| Accuracy | 5(1)(d) | Agent output must not distort facts; humans verify |
| Storage limitation | 5(1)(e) | No logging of raw personal data at the provider; retention for the mapping table |
| Integrity & confidentiality | 5(1)(f) | Security measures → F |
| **Accountability** | 5(2) | Controller must "be able to demonstrate compliance" → the **test protocol** is the evidence |

---

## C. Legal basis (Art. 6) → condition for ALLOW

Processing is lawful only if **at least one** applies: (a) consent · (b) necessary for a contract / pre-contractual steps at the data subject's request (e.g. a job application) · (c) legal obligation · (d) vital interests · (e) public interest / official authority · (f) legitimate interests, unless overridden by the data subject's rights.

Art. 6(4) — the compatibility test for further processing lists "**encryption or pseudonymisation**" as an appropriate safeguard.

**Use:** for each data category in the policy matrix, name the Art. 6 basis. No basis → BLOCK. In recruiting, 6(1)(b) (pre-contractual steps) is the usual choice; 6(1)(f) needs a balancing test and opens the Art. 21 right to object.

---

## D. Special categories (Art. 9) and criminal data (Art. 10) → BLOCK / LOCAL ONLY

Prohibited by default: racial/ethnic origin, political opinions, religious/philosophical beliefs, trade-union membership, genetic data, biometric data (for identification), **health data**, sex life / sexual orientation.

Exceptions (Art. 9(2)): explicit consent (a), employment/social-security law (b), vital interests (c), data manifestly made public (e), legal claims (f), substantial public interest (g), health care under secrecy (h), public health (i), research (j).

**Use:** detect these categories in free text and **BLOCK transfer to the external model** (the "medical disclosure in the middle of a CV" test). LOCAL ONLY only if a 9(2) exception is documented.

**Art. 10:** criminal convictions and offences may be processed only "under the control of official authority" or when authorised by law with safeguards → treat like Art. 9: **BLOCK**.

---

## E. Automated decisions & human oversight (Art. 22, Recital 71, Art. 21)

- Art. 22(1): right "not to be subject to a decision based solely on automated processing, including profiling", with legal or similarly significant effects.
- Recital 71 explicitly cites "**e-recruiting practices without any human intervention**" and automatic refusal of online credit.
- Exceptions (22(2)): contract necessity, law, explicit consent — then (22(3)) at least **human intervention**, the right to express one's view and to **contest the decision**.
- Art. 22(4): such decisions must not be based on Art. 9 data unless 9(2)(a) or (g) applies.
- Recital 71: right "to obtain an explanation of the decision"; "appropriate mathematical or statistical procedures"; prevent "discriminatory effects" (origin, opinion, religion, union, genetic/health status, sexual orientation). Not for children.
- Art. 21: if the basis is 6(1)(e) or (f), the data subject can **object**, including to profiling.

**Use:** "Final decision → no autonomous decision by the agent". The agent prepares, a human decides. Output must be **explainable** (which criteria were matched) and never use Art. 9 attributes → also a bias/fairness argument for the jury.

---

## F. Privacy by design & security (Art. 25, Art. 32, Recitals 28–29) → PROTECT

- Art. 25(1): measures "such as pseudonymisation" to implement principles "such as data minimisation".
- Art. 25(2): by default, only data "necessary for each specific purpose" (amount, extent, storage, accessibility).
- Art. 32(1): "(a) the pseudonymisation and encryption of personal data", confidentiality/availability/resilience (b), and "(d) a process for regularly testing, assessing and evaluating" the measures.
- Recital 28: pseudonymisation reduces risk but doesn't preclude other measures.
- Recital 29: pseudonymisation within the same controller is possible if the re-identification info is kept separately and **authorised persons** are named → define who can open the `CANDIDATE_01` ↔ person table.

**Use:** pseudonymise names, remove emails/phones at **every occurrence** (Repeated-details test). Art. 32(1)(d) justifies the **5 security tests** and **fail-closed** behaviour. Prompt-injection resistance (Bypass test) = integrity and confidentiality (Art. 5(1)(f)).

---

## G. Sending data to an external AI model (Art. 28, Art. 44–46)

- Art. 28: only processors "providing sufficient guarantees"; written contract (DPA) required; no sub-processors without authorisation.
- Art. 44: transfer to a **third country** (e.g. US-hosted model) only if Chapter V conditions are met.
- Art. 46: without an adequacy decision → appropriate safeguards (e.g. Standard Contractual Clauses). Art. 45 adequacy (EU–US Data Privacy Framework) to be verified separately.

**Use:** strongest argument for minimising what reaches OpenAI → anything not needed is removed **before** it leaves the EU environment. Fully re-identifiable data → LOCAL ONLY.

---

## H. Risk, transparency & records (Art. 35, Art. 13, Art. 30)

- Art. 35(1): **DPIA** where processing, "in particular using new technologies", is likely high-risk.
- Art. 35(3)(a): mandatory for "systematic and extensive evaluation of personal aspects … based on automated processing, including profiling"; 35(3)(b): large-scale Art. 9 data.
- Art. 13: at collection, inform data subjects of controller identity, purposes, **legal basis**, recipients…
- Art. 30: **record of processing activities** (purposes, categories of data subjects and data, recipients incl. third countries, transfers…).

**Use:** a real deployment needs a DPIA and an updated privacy notice naming the AI processing. The BRANE test protocol = technical part of the Art. 30 record and of the Art. 5(2) evidence.
