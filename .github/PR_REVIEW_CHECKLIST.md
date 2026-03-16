# Lucidity PR Review Checklist

Use this checklist when reviewing convergence and feature PRs.

## Product shape
- [ ] Does the PR reinforce Lucidity as a **local-first, auditable Dream Mode memory system**?
- [ ] Is the default user path clear?
- [ ] Are Dream Mode vs advanced/custom paths easy to distinguish?

## Safety model
- [ ] Are backups/manifests/rollback preserved?
- [ ] Is autonomous promotion bounded by explicit policy?
- [ ] Is episodic memory preserved/searchable without being over-canonized?
- [ ] Are sensitive or contradictory cases kept conservative?

## Installer / operations
- [ ] Do installer prompts match the intended product behavior?
- [ ] Do cron jobs point only at scripts that actually exist in-repo?
- [ ] Are reporting defaults quiet unless explicitly configured otherwise?

## Docs consistency
- [ ] Root README, skill README, SKILL.md, INSTALL, and GATEWAY_CRON agree with each other
- [ ] Any new concepts are documented once clearly and referenced consistently
- [ ] Changelog and version metadata reflect the actual shipped behavior

## Verification
- [ ] `bash -n skills/lucidity/install.sh`
- [ ] Python syntax/compile checks pass for changed scripts
- [ ] `test_apply_idempotency.py` still passes when apply logic is touched
- [ ] CI passes on branch + PR

## Repo hygiene
- [ ] Only Lucidity/Anima-related files are present in this repo
- [ ] No unrelated skills, debate artifacts, private corpora, or stray runs are tracked
- [ ] Release tags and GitHub releases are updated when versioned behavior changes land
