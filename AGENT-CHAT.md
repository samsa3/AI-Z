# Agent Shared Chat Log

Purpose: A place for multiple agents to "talk" to each other and to the human, coordinating work in this repo.

> Use this file for discussion, questions, status updates, and hand‑offs.
> Use `AGENT-PLAN.md` for the structured plan and task board.

---

## 0. Protocol for Agents

When writing here, follow this format so other agents can parse it easily:

```text
[YYYY-MM-DD HH:MM UTC] @agent-name (role): short one‑line summary

Longer explanation if needed...

- Bullet points for status / findings
- Questions for other agents or for the human

Next actions:
- [ ] TODO 1
- [ ] TODO 2
```

Guidelines:

1. Always include a timestamp and agent name.
2. Keep each entry small and focused on a single topic.
3. If you change the plan, also update `AGENT-PLAN.md`.
4. When handing off, clearly say: `Handoff to @agent-name: ...`.
5. Assume this log is append‑only; do not rewrite past entries.

---

## 1. Active Conversation

Append new messages at the bottom of this section. Do not edit older messages except to fix obvious formatting errors.

Example template entry:

```text
[2026-11-20 13:00 UTC] @hermes-agent (coding):

Investigated repo structure and confirmed BRANE integration must wrap all model calls.

Findings:
- AGENTS.md defines non‑negotiable rules.
- Agent code lives under `agent/`.

Questions:
- Should we prioritize the legal research docs or the agent code next?

Next actions:
- [ ] Wait for human to set priorities.
```

[2026-11-20 15:25 UTC] @rodrigo-claude (agent dev): prototype agent pipeline + T1-T5 tests pushed on branch `agent/policy-engine-prototype`

Who: Claude assistant working for Rodrigo (GitHub @Rocasigle). Task: agent policy engine + BRANE gateway prototype.

What exists on the branch (not merged to `main`):
- `agent/brane_agent/policy.py` + `agent/policies.json`: local policy layer, rule IDs = `docs/03-policy-matrix.md`. R2 names -> stable `PERSON_nn` at every variant ("M. Fictus", "Ms Fictus", "Fictus, Mira"); R3 email/phone/url/address removed; R5 IBAN/ID removed; R6/R7 sentences with special-category / criminal data removed; R9 sentences with embedded instructions removed.
- Egress check: the exact outbound payload is re-scanned; any remaining hit -> BLOCK, nothing sent.
- `agent/brane_agent/gateway.py`: BRANE is the only model path. No OpenAI client in the code. Any error / timeout / missing config -> R10 BLOCK, no fallback.
- `pipeline.py`: output = recommendation + human-review notice (R12); re-identification only locally; `logs/audit.jsonl` (R13, pseudonyms only) and `mappings/` (R8) are git-ignored.
- `data/synthetic/01..05_*.txt` + `tests/security/test_security.py`.

Verification actually run:
- `python -m unittest discover -s tests/security -t .` -> 8/8 OK (T1, T2, T3, T4, T5 x3 variants, no-direct-OpenAI check), against a LOCAL MOCK gateway that records what it receives.
- CLI run on all 5 inputs: no name, email, phone, health detail, IBAN or injection text in the payload; task content still passes.

NOT verified:
- Real BRANE behaviour/API. `gateway.py` ASSUMES an OpenAI-compatible `POST {BRANE_API_URL}/v1/chat/completions` with Bearer key. Only `_build_request` / `_parse_response` need changing once we have the docs.
- Name detection needs a label line, an honorific or `known_names`; special-category detection is keyword-based (misses paraphrases) -> BRANE's own detection must cover that.
- Synthetic data and criteria follow the recruiting example only because the use case is still TODO.

Questions:
- Who has BRANE credentials / API docs? (also in Parking Lot)

Handoff to whoever has BRANE access: please run `python -m agent.brane_agent.cli data/synthetic/02_protected.txt --show-payload` WITHOUT `--mock` and report what BRANE returns, so we can fix the gateway adapter.

Next actions:
- [ ] Adapt gateway to the real BRANE API
- [ ] Adapt `policies.json` + synthetic data once the use case is confirmed

[2026-11-20 15:40 UTC] @rodrigo-claude (agent dev): docs synced with prototype; BRANE has no public API docs

- Branch `agent/policy-engine-prototype` now also updates `docs/03-policy-matrix.md` (Implemented? column) and `tests/test-protocol.md` (T1–T5 = PASS against **mock** gateway, run log entry).
- `AGENTS.md` on `main`: Current status, Stack, Decisions log (own local policy layer in front of BRANE — proposal, please object here if you disagree), Session log.
- Searched for BRANE API docs: only product/marketing pages from AI-Z Group; the technical whitepaper is behind a registration form. The gateway adapter stays an ASSUMPTION until the organisers give us credentials + docs.

Questions:
- Is anyone else (Charly, samsa3, other agents) already building agent code? If yes, reply here before we both write the same thing.

Handoff to whoever gets BRANE access from the organisers: please post the endpoint format / auth / block response here (no keys!), and I will adapt `gateway.py`.

---

## 2. Parking Lot / Questions for Human

Agents can collect questions here that require human decisions.

- [ ] TODO — asked by @agent-name on YYYY‑MM‑DD
- [ ] Which use case do we build? Code is use-case agnostic but data/criteria currently follow the recruiting example — asked by @rodrigo-claude on 2026-11-20
- [ ] Who has BRANE credentials and API documentation (endpoint, auth, block response format)? — asked by @rodrigo-claude on 2026-11-20

When the human answers, add the answer inline under the question.

---

## 3. Notes / Misc

Scratch space for short notes that don't fit anywhere else. Clean up periodically to keep this file readable.
