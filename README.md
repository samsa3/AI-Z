# AI-Z Challenge — MAIN Summit 2026 (Maastricht, 20–21 Nov)

> **Build the Agent. Define the Rules. Make It Work.**
> An AI agent for a legally demanding business process, with BRANE (AI firewall) enforcing our data-protection rules before anything reaches OpenAI.

## Our use case
_TODO — one paragraph: the business process, the data involved, the expected output, who keeps the final decision._ → details in [`docs/01-use-case.md`](docs/01-use-case.md)

## Team
| Name | GitHub | Role |
|---|---|---|
| Charly Perrin | @charly4perrin-jpg | |
| | @samsa3 | |
| | | |
| | | |

## Deliverables (what the jury sees)
| # | Deliverable | Where | Owner | Status |
|---|---|---|---|---|
| 1 | Working AI agent with BRANE | [`agent/`](agent/) | | ⬜ |
| 2 | Legal research with sources | [`docs/02-legal-research.md`](docs/02-legal-research.md) | | ⬜ |
| 3 | Policy matrix | [`docs/03-policy-matrix.md`](docs/03-policy-matrix.md) | | ⬜ |
| 4 | Live demo & business case | [`docs/04-business-case.md`](docs/04-business-case.md) | | ⬜ |
| — | Test protocol (5 security tests) | [`tests/test-protocol.md`](tests/test-protocol.md) | | ⬜ |

## Minimum requirements (checklist)
- [ ] Self-selected, legally demanding, fundamentally permissible use case
- [ ] ≥ 3 justified **and implemented** protection rules
- [ ] 5 documented test cases (control, protected data, repeated details, bypass, check failure)
- [ ] Concrete, verifiable legal sources for key decisions
- [ ] Agent can perform its task repeatedly
- [ ] Synthetic data only

## Scoring
Technology & Execution **40** · Legal Research & Governance **40** · Business Impact **20**
+ 5 pass/fail security tests — **a single impermissible transfer = failed**.

## Repo layout
```
agent/            agent code (BRANE + OpenAI)
docs/             use case, legal research, policy matrix, business case
tests/            test protocol + test scripts
data/synthetic/   synthetic inputs for each test case
```

## Timeline
- **Fri 20 Nov** — use case, legal research, policies, first agent version
- **Sat 21 Nov** — tests, final implementation, presentation

How we work together: see [`CONTRIBUTING.md`](CONTRIBUTING.md).
