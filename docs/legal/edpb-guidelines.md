# EDPB guidelines

Overview: [`../02-legal-research.md`](../02-legal-research.md).

## 1. WP29 / EDPB — Guidelines on automated decision-making and profiling (WP251 rev.01)
Summary — **verify wording in the original**:
- Art. 22(1) GDPR is read as a **general prohibition** of solely automated decisions with legal/similarly significant effects, not only a right to invoke.
- Not "solely automated" only if human involvement is **meaningful**: the reviewer has authority and competence to change the decision and actually considers all relevant data. A "rubber stamp" doesn't count.
- Automatic rejection of job applicants is a typical "similarly significant effect".
- Controllers should explain the logic involved and test for errors and bias.

→ Technical rule: the HR reviewer sees the original (re-identified) application, not only the AI summary, and records their own decision.

Source: search "WP251rev.01" on the EDPB / European Commission site.

## 2. EDPB — Guidelines 01/2025 on pseudonymisation
Adopted 16 January 2025 for public consultation (**check whether a final version was published**).
- Pseudonymised data **remains personal data**; only anonymised data falls outside the GDPR (consistent with Recital 26).
- Key risk-reduction measure; can support reliance on **legitimate interest** (Art. 6(1)(f)) and compatibility of further processing (Art. 6(4)).
- Effectiveness depends on keeping the **additional information** (re-identification key) separate and protected, and on who can access it.
- **"Pseudonymisation domain"**: the set of actors from whom the data should not be attributable to a person.

→ Policy matrix: pseudonymisation domain = OpenAI (external model). The `CANDIDATE_01` ↔ person table stays LOCAL ONLY with named authorised staff (GDPR Recital 29). Also replace **indirect identifiers** (employer names, rare job titles, exact dates) when they could single out a person.

Sources:
- Summary: https://edpb.europa.eu/system/files/2025-02/edpb_summary_202501_pseudonymisation_en.pdf
- Consultation page: https://www.edpb.europa.eu/our-work-tools/documents/public-consultations/2025/guidelines-012025-pseudonymisation_en
- Commentary: https://stibbe.com/publications-and-insights/key-takeaways-and-insights-from-the-edpb-pseudonymisation-guidelines
