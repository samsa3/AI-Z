# Agent

Code of the AI agent. Every model call goes through BRANE — no direct call to OpenAI.

- [ ] Choose stack (Python recommended)
- [ ] BRANE client + config of our policies
- [ ] Agent logic (input → BRANE → OpenAI → output)
- [ ] Fail-closed: if BRANE is unreachable, nothing is sent (no cloud fallback)
- [ ] Log every decision (allow / protect / local only / block) for the test protocol

## GDPR requirements the code must implement
Source: GDPR — https://eur-lex.europa.eu/eli/reg/2016/679/oj

| Requirement | Article | In the code |
|---|---|---|
| Data protection by design & by default | Art. 25 | BRANE is called **before** every model request, by default, no flag to disable it |
| Minimisation | Art. 5(1)(c) | Only task-relevant fields are put in the prompt |
| Pseudonymisation, key kept separately | Art. 4(5), 32(1)(a) | Token mapping stored locally (`mappings/`, git-ignored), never in prompts or logs |
| Security / fail closed | Art. 32 | Any BRANE error or timeout → abort, no fallback to OpenAI |
| Special categories never leave | Art. 9 | Blocked by BRANE policy; request aborted if still detected |
| Human decision | Art. 22 | Output = recommendation + "requires human review" flag |
| Accountability | Art. 5(2), 30 | Structured log per request: timestamp, policy applied, decision, pseudonyms only |
| Storage limitation | Art. 5(1)(e) | Don't persist raw inputs/outputs longer than needed |

## AI Act requirements the code must implement
Source: [`../docs/legal/ai-act.md`](../docs/legal/ai-act.md)

| Requirement | Article | In the code |
|---|---|---|
| Human oversight | AI Act Art. 14 | Output = **recommendation with reasons**, never a verdict; reviewer can override; stop/kill-switch |
| Automation bias warning | Art. 14(4)(b) | UI/output reminds the reviewer not to rely blindly on the result |
| Explanation | Art. 86 + GDPR Rec. 71 | Log which criteria were matched for each person |
| No emotion inference | Art. 5(1)(f) | Never analyse tone, video or "personality" |
| Meaningful review | EDPB WP251 | Reviewer can see the original (re-identified) input locally and records their own decision |
