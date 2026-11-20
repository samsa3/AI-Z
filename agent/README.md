# Agent

Code of the AI agent. Every model call goes through BRANE — no direct call to OpenAI.

- [ ] Choose stack (Python recommended)
- [ ] BRANE client + config of our policies
- [ ] Agent logic (input → BRANE → OpenAI → output)
- [ ] Fail-closed: if BRANE is unreachable, nothing is sent (no cloud fallback)
- [ ] Log every decision (allow / protect / local only / block) for the test protocol
