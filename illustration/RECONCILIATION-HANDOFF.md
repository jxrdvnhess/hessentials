# Branch Reconciliation — final handoff (2026-06-17)

The scary part was already over by June 13. As of today it's **smaller still**: the live-art
generators are already on GitHub, so this is pure optional archiving + cleanup.

## State confirmed today
- `main` == `origin/main` == `550108a` (live, complete, current). Unchanged.
- The painter generators that produce the live About art (`about_figure.py`, `about_scenes.py`,
  `about_frame.py`, `line_figure.py`) and ~580 other `illustration/` files are **already
  committed to `main`** — i.e. already on GitHub. The June-13 briefing's main worry is resolved.
- The only thing not yet on GitHub: additional research *source* (Sketch 501 notes, Human
  Studies Vol.1, `production/` batches, candidate explorations) + 95 MB of regenerable renders.

## What I staged in the working tree (Cowork can't commit — you do that)
- Materialized **56 source files** (`.py` / `.md`) into `illustration/` — the research not yet
  on `main`. These show as new untracked files.
- Edited `illustration/.gitignore` to ignore `samples/` and `**/out/` so the **95 MB of
  regenerable renders are not committed**. Verified: `git add illustration` stages 56 source
  files and **zero PNGs**.
- Touched nothing under `src/`, `content/`, or `public/`. The only modified tracked file is
  `illustration/.gitignore`.

## Your steps (run on your Mac — native, not the sandbox)

```
# 1. Remove the stale lock my read-only git commands left behind (sandbox couldn't delete it)
rm -f ~/hessentials/.git/index.lock

# 2. Stage source + the gitignore change (gitignore excludes renders automatically)
cd ~/hessentials
git add illustration
git status          # confirm: ~56 new .py/.md + modified .gitignore, ZERO .png, no Personal Photos

# 3. Commit
git commit -m "illustration: archive research source (generators + notes); ignore sample renders"

# 4. Push  — GitHub Desktop "Push origin" (authed). Touches only illustration/ + .gitignore,
#    so the live site is unaffected; Vercel build should pass.

# 5. Retire the old backup branch (Desktop folder backup also exists)
git branch -D backup-local-work
```

## Hazards (these bit the earlier sessions)
- **Never force-push. Never merge `backup-local-work` into `main`** — it would drag back the
  rewritten history and the personal media.
- **`Personal Photos/` stays out** — still gitignored; never commit it. The 130 MB video there
  once blocked the push (GitHub's 100 MB cap).
- Local `npm run dev` chokes if `Personal Photos/` is present (Tailwind v4 scans it). Keep it
  moved out (`~/Desktop/hessentials-personal-photos`); `rm -rf .next` after.
- The untracked dev-preview routes under `src/app/illustration-flow/` (about-decision, july,
  sprint-b/c/d) are left alone — not deployed, local only. Clean them whenever you like.
```
