# Security Policy

## Reporting a vulnerability

If you believe you’ve found a security issue in Lucidity, please report it privately.

- Preferred: open a GitHub Security Advisory (if enabled for the repo)
- Otherwise: contact Gottschling Labs maintainers directly

Please include:
- a clear description of the issue
- impact assessment (what could go wrong)
- steps to reproduce
- any suggested fix

## Scope

Lucidity focuses on local-first scripts and documentation.

In scope:
- unintended destructive behavior
- data exfiltration risks
- unsafe default configurations
- path traversal / arbitrary file overwrite
- mishandling of sensitive tiers

Out of scope:
- vulnerabilities in OpenClaw itself (report upstream)
- OS-level compromise not caused by Lucidity

## Coordinated disclosure

We prefer coordinated disclosure and will acknowledge reports as quickly as possible.
