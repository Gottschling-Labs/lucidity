# Git remote and push path (Ops Deck nightshift)

Date: 2026-02-16
Tags: research, git, ops, process, ops-deck

## Situation

This workspace has a git repository and an `ops-deck-ui` branch, but it has no git remote configured.

That means NIGHTSHIFT can commit locally but cannot push. The wagon can roll, but it cannot leave the ranch.

## What I saw

- `git branch --show-current` -> `ops-deck-ui`
- `git remote -v` -> no output
- The repo contents look like notes and mission-control docs, not an actual UI project (no `package.json` in the top couple levels).

## Why it matters

Ops Deck tasks that say "commit + push to ops-deck-ui" need a boring, repeatable remote target:

- correct remote URL
- correct default branch
- correct expectation for what lives in this repo (UI code vs notes)

Without that, a push attempt becomes a guess. Guesses turn into fires.

## Proposed boring solution

1) Confirm the canonical remote URL for this repo.
2) Confirm whether the Ops Deck UI lives here or in a separate repo.
3) Lock a convention:
- notes changes can land on `master` (or `main`)
- UI changes land on `ops-deck-ui` (or in a dedicated UI repo)

Once the remote is known, NIGHTSHIFT can push cleanly and keep receipts tight.

## Safe next step

Add a single approval item: "tell me the remote URL and where the UI lives". Then wire it and move on.
