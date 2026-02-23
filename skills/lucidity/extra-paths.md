# Lucidity - Extra memory indexing paths (optional)

Some OpenClaw deployments allow configuring additional file paths for memory indexing beyond the defaults.

Use this carefully.

## Principles

- Indexing scope should be broader than injection scope.
- Do not index secrets.
- Prefer small, stable, high-signal markdown.

## Suggested candidates (examples)

- `skills/lucidity/` (docs and policies)
- `skills/lucidity/memory-architecture/` (design deck)

## What to avoid

- `.git/`
- `node_modules/`
- logs
- large generated artifacts

See also: `skills/lucidity/memory-architecture/indexing-inputs.md`
