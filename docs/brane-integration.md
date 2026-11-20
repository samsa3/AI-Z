# BRANE integration — verified facts

Source: organiser mail (AI-Z Group, 20 Nov 2026) + our own calls against the team endpoint on 2026-11-20.
**Never put the API key or the chat login in this repo.** They live in `.env` (git-ignored) only.

## Access
| Item | Value |
|---|---|
| Team | LarpAI (department starts **fully open**: all 25 categories = "Send as Typed") |
| Base URL | `https://brane.ai-z.io/api/v1` → env `BRANE_BASE_URL` |
| Auth | `Authorization: Bearer $BRANE_API_KEY` (one team key, from the organiser mail) |
| Policy workbench | `https://brane.ai-z.io/team-policy` (paste the key; has a one-click "floor" preset) |
| Build tag | env `TEAM_BUILD="LarpAI / policy-v1"` |
| Deadline | **Sat 21 Nov 2026, 10:30 CET** — hand in 2 CSVs: policy matrix, and tests T1–T5 + our 5 edge cases (templates in the organiser's starter-kit zip) |

## Models (`GET /models`, verified)
| Model id | Where it runs |
|---|---|
| `openrouter:anthropic/claude-haiku-5.5` (default, or `auto`) | cloud |
| `openrouter:openai/gpt-6-luna` | cloud |
| `openrouter:mistralai/mistral-large-4-0` | cloud |
| `vllm:deepseek-v4.1-flash` | **local, no cloud egress** → candidate for LOCAL ONLY |
| `vllm:qwen3.8-27b-nvfp4` | **local, no cloud egress** → candidate for LOCAL ONLY |

## API behaviour (verified)
- OpenAI-compatible: `POST {base}/chat/completions`, `GET {base}/models`.
- BRANE reports its decision in **response headers** — we store them in `logs/audit.jsonl` (`"brane"` field):
  `x-brane-action` (seen: `allow`), `x-brane-lane` (`governed`), `x-brane-pii-detected`, `x-brane-redacted`, `x-brane-routed-to` (`cloud`), `x-brane-model-resolved`.
- Invalid key → HTTP 401 → our gateway blocks (R10).
- Cloudflare in front of BRANE rejects Python's default `User-Agent` with **HTTP 403 "error code: 1010"** — this is NOT a BRANE policy block. `gateway.py` sends `larpai-agent/0.1 (...)`.

## Not yet verified
- What BRANE returns when **it** blocks / redacts / routes local (status code, headers, body).
- Behaviour per policy category once the workbench policy is set (currently fully open, so BRANE alone would forward everything — our local layer is what protects today).
- Contents of the organiser starter kit / README / CSV templates (zip not yet in the repo).
