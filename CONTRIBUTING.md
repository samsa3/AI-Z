# How we work on this repo

## Golden rules
1. **Pull before you start**, push often (at least every hour) so everyone sees progress.
2. **Never commit secrets** — API keys go in `.env` (ignored). Use `.env.example` as template.
3. **Synthetic data only** — no real names, emails, contracts.
4. Non-coders can edit `docs/` directly on github.com (pencil icon → "Commit changes").

## Branches
- `main` = always working, demo-ready.
- One branch per task: `legal/gdpr-basis`, `agent/brane-client`, `tests/bypass-case`…
- Small doc fixes can go straight to `main`.

## Flow
```bash
git pull origin main
git checkout -b agent/brane-client
# ... work ...
git add .
git commit -m "agent: add BRANE client with fail-closed check"
git push -u origin agent/brane-client
```
Then open a Pull Request on GitHub → one teammate glances at it → merge.

## Commit messages
`<area>: <what changed>` — areas: `agent`, `legal`, `policy`, `tests`, `data`, `docs`.

## Tracking tasks
Use **GitHub Issues** (one issue per task, assign yourself) and update the status column in the README.
