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

---

## 2. Parking Lot / Questions for Human

Agents can collect questions here that require human decisions.

- [ ] TODO — asked by @agent-name on YYYY‑MM‑DD

When the human answers, add the answer inline under the question.

---

## 3. Notes / Misc

Scratch space for short notes that don't fit anywhere else. Clean up periodically to keep this file readable.
