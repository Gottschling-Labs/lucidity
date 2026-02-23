# Lucidity - Sandboxing guide

This document describes recommended sandboxing patterns for running Lucidity scripts.

Lucidity scripts are local-first and primarily operate on Markdown files. Sandboxing is recommended before public release to reduce the impact of mistakes (wrong paths) and limit file access.

## 1) Goals

- Prevent writes outside the intended workspace root.
- Prevent reads of unrelated user files.
- Make automation safer.

## 2) Minimal sandbox approach (container)

A practical approach is to run the scripts in a container with a single mounted workspace directory.

Example (conceptual Docker/Podman pattern):

- Mount the target workspace as `/workspace`.
- Run scripts with `--workspace /workspace`.
- Do not mount your home directory.

Pseudo-command:

```bash
podman run --rm \
  -v "$HOME/.openclaw/workspace:/workspace:Z" \
  -w /workspace \
  python:3.12-slim \
  python3 /path/to/lucidity/skills/lucidity/memory-architecture/scripts/distill_daily.py --workspace /workspace --date 2026-02-23
```

Notes:
- This repo does not ship a container image yet. If we add one, it should be pinned and minimal.
- SELinux label flags (e.g., `:Z`) may be needed on some systems.

## 3) Read-only mounts where possible

For staging-only runs (distill/dedupe dry-run), you can mount the workspace read-write but consider making non-target paths read-only.

For apply runs, the workspace must be writable, but you can still avoid mounting anything else.

## 4) Alternative sandboxing

- Use a dedicated OS user with permissions limited to the workspace directory.
- Use filesystem ACLs to deny access outside the workspace.

## 5) What to verify

- Running with `--workspace` points to the intended root.
- Outputs land under `/workspace/memory/staging/`.
- No access to `$HOME` or other directories is granted.

## 6) Disclaimer

This is guidance, not a guarantee. The safest practice is still:
- staging-first
- dry-run first
- backups before apply
