---
name: debate-orchestrator
version: 0.1.0
description: "Orchestrate multi-role debates (Proponent/Critic/Fact-Checker/Executor) in OpenClaw with persisted transcripts and safe defaults."
metadata:
  openclaw:
    emoji: "⚖️"
    requires:
      bins: ["python3"]
---

# Debate Orchestrator

This skill provides a runnable orchestrator for conducting multi-role debates using OpenClaw sub-sessions.

## Status

MVP scaffold: creates the skill bundle and a CLI entrypoint. Orchestration logic is implemented incrementally in the project plan.

## Run

```bash
python3 skills/debate-orchestrator/scripts/debate.py --help
```

## Docs

- Spec: `debate-architecture/spec.md`
- Role prompts: `debate-architecture/templates/role-prompts.md`
- Transcript conventions: `debate-architecture/templates/transcript-conventions.md`
