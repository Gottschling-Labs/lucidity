# Contributing to Lucidity

Thanks for your interest in improving Lucidity.

## Ground rules

- Be respectful and assume good intent.
- Prefer small PRs with clear scope.
- Keep changes **local-first** and **reversible** by default.

## Development workflow

1. Fork the repo (or create a branch if you have write access).
2. Make changes.
3. Run basic checks:

```bash
python3 -m compileall -q skills/lucidity/memory-architecture/scripts
python3 skills/lucidity/memory-architecture/scripts/test_apply_idempotency.py
```

4. Open a PR with:
- what changed
- why
- how you tested

## What we accept

- Documentation improvements
- Safety hardening
- Better schemas and distillation heuristics
- Test coverage (especially idempotency / rollback)

## What we avoid

- Default-on destructive behaviors
- Hidden network calls or telemetry by default
- Storing secrets in always-loaded tiers

## License

This project is licensed under **GPL-3.0-or-later**. By contributing, you agree that your contributions are provided under the same license.
