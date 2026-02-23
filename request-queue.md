# Request Queue and Wish List

Purpose: capture proposed improvements that need Brandon approval before implementation.

## Pending approval

### 8) Fix web research plumbing (keys plus browser tool)
- Observation: `web_search` is currently blocked by `missing_brave_api_key`, and the `browser` tool cannot reach the browser control service (timeout).
- Proposal: set up either Brave or Perplexity keys, then restart the gateway to bring `web_search` back. Also investigate why the browser control service is unreachable.
- Why: NIGHTSHIFT research work is crippled without search or a working browser.
- Risk: low to medium (touches keys and gateway restart, but reversible).

### 4) Multi-model routing policy
- Proposal: formalize model routing rules: cheap model for routine tasks, stronger model only when needed, with explicit budget limits.
- Why: reduce token burn.
- Risk: medium (quality regressions if routing is too aggressive).

### 5) Memory hygiene architecture
- Proposal: explicit cadence and tooling for distillation from daily notes to curated memory, plus a "forget by default" stance on volatile details.
- Why: keeps context lean and accurate.
- Risk: medium (could drop useful nuance if done too bluntly).

### 7) Git remote and push target for Ops Deck work
- Observation: this workspace repo currently has no git remote configured, so I cannot actually push `ops-deck-ui`.
- Current impact: I can commit locally, but `git push` fails. There are now multiple local commits waiting to be pushed (latest: `d2a3d66`).
- Also: the repo contents look like notes and mission-control docs, not a UI project (no `package.json` in the top couple levels).
- Proposal: confirm the canonical remote URL and confirm whether the Ops Deck UI lives in this repo or a separate one.
- Why: NIGHTSHIFT needs a safe, repeatable push path.
- Risk: low (process), but mispointing the remote would be ugly.

## Approved and in progress

> Nightshift rule: keep this section current. Add a short **Progress** note with timestamps as work happens. When done, move the item to **Completed** and include links to commits/PRs.

### Memory architecture (Phase 1)
- Queued: define the minimal evaluation harness and scoring rubric (create `workspace/memory-architecture/eval-harness.md`).

### 0) Use browser relay for research
- Approved: use the Chrome Relay browser for research tasks.

### 0b) Git remote plus branch conventions for Ops Deck work
- Approved: standardize repo locations and branch conventions so nightshift pushes cleanly.

### 1) Distilled notes sync pipeline
- Approved: build tooling to distill local raw notes into repo versioned notes.

### 2) Ops Deck UI: markdown viewer and note index
- Approved: implement index and markdown rendering for distilled notes, with tags and search.
- Progress (2026-02-16 22:54 ET): Sorted Research list by file modified time and added a last-updated date stamp in the list. Commit: 02ccbcf (ops-deck-ui).
- Progress (2026-02-16 23:18 ET): Added tag parsing plus a tag dropdown filter on /research. Also shows title and tag badges in the list. Commit: 66ffb1d (ops-deck-ui).
- Progress (2026-02-16 23:32 ET): Search now matches tags as well as filename and title. Commit: 1a775b3 (ops-deck-ui).
- Progress (2026-02-16 23:46 ET): Tag badges in the distilled list are now clickable. Clicking a tag jumps to /research filtered by that tag (and preserves the current search query). Commit: 11b7d21 (ops-deck-ui).
- Progress (2026-02-16 23:58 ET): Research index now parses YAML frontmatter for title and tags (supports inline list, comma list, or YAML dash list), falling back to H1 and a "Tags:" line. Commit: b411ebf (ops-deck-ui).
- Progress (2026-02-17 00:13 ET): Tag dropdown now shows counts per tag, so you can see how much ground each filter covers before you pull the trigger. Commit: 8eafccf (ops-deck-ui).
- Progress (2026-02-17 00:26 ET): Research list now uses note title as the primary link label, carries current q and tag into the note URL, and the note page Back link returns you to the same filtered list. Also shows parsed title and tags on the note page. Commit: a172a10 (ops-deck-ui).
- Progress (2026-02-17 00:41 ET): Research search now matches note content (first 20k chars), not just filename, title, and tags. Commit: 5512fd7 (ops-deck-ui).
- Progress (2026-02-17 00:54 ET): Research list now shows a short excerpt snippet when your search query matches note content, so you can spot the right file quicker. Commit: 7587849 (ops-deck-ui).
- Progress (2026-02-17 01:14 ET): Highlighted search query matches in the Research list title and excerpt, so the right note jumps out quicker. Commit: a11387c (ops-deck-ui).
- Progress (2026-02-17 01:31 ET): Research index now reads only a small head slice (64 KB) of each distilled note instead of the full file, keeping the list route fast even if notes get chunky. Commit: 48f4f62 (ops-deck-ui).
- Progress (2026-02-17 01:39 ET): Research header now shows filtered count versus total files so you can tell when filters are narrowing the list. Commit: 9d0c1ec (ops-deck-ui).
- Progress (2026-02-17 01:54 ET): Research page now shows Active filter chips for q and tag, each removable with one click. Commit: d18c07c (ops-deck-ui).
- Progress (2026-02-17 02:09 ET): Research list now shows a "+N more" chip when a note has more than 6 tags, with a tooltip listing all tags. Commit: 749e0db (ops-deck-ui).
- Progress (2026-02-17 02:28 ET): When Research filters yield zero results, the page now offers clear filter links so you can get unstuck fast. Commit: f09a223 (ops-deck-ui).
- Progress (2026-02-17 02:46 ET): Added keyboard shortcut support on /research. Press "/" to focus search, Esc to drop focus. Commit: 6dd3869 (ops-deck-ui).
- Progress (2026-02-17 02:58 ET): Added a Sort dropdown on /research (Recent or Title) and preserved sort across note links and Back. Commit: 2c047f3 (ops-deck-ui).
- Progress (2026-02-17 03:09 ET): Added an inline hint next to Search showing the "/" and Esc shortcuts. Commit: ffefb3f (ops-deck-ui).
- Progress (2026-02-17 03:24 ET): When a search matches filename, title, or tags but not note content, the list now shows a small hint so the lack of excerpt makes sense. Commit: 3507357 (ops-deck-ui).
- Progress (2026-02-17 03:39 ET): Research search now supports multi-word queries. It matches all terms across meta or content, and highlights each term in titles and excerpts. Commit: 7cb1470 (ops-deck-ui).
- Progress (2026-02-17 03:56 ET): Excerpt generation now centers on the earliest matching search term, so snippets are less misleading when the first query term is not the first hit. Commit: 1e078a0 (ops-deck-ui).
- Progress (2026-02-17 04:15 ET): Added a small inline "Clear q" control next to the search box (and set the input type to search), so you can drop the query without losing tag or sort. Commit: 31b203c (ops-deck-ui).
- Progress (2026-02-17 04:27 ET): On /research, Esc now clears the search box if it has content. If the box is already empty, Esc blurs it. Commit: e672d46 (ops-deck-ui).
- Progress (2026-02-17 04:39 ET): On /research, Ctrl/Cmd+K now focuses the search box (same behavior as "/"). Also updated the shortcut hint copy. Commit: 2855b1b (ops-deck-ui).
- Progress (2026-02-17 04:57 ET): Esc on /research now clears the query and refreshes the list immediately, so it behaves like a fast "Clear q". Commit: 69c04ed (ops-deck-ui).
- Progress (2026-02-17 05:18 ET): /research now tolerates a missing ops-notes/distilled directory (shows empty state instead of 500). Commit: 99eb96a (ops-deck-ui).
- Progress (2026-02-17 05:24 ET): Added a Copy link button on /research/[slug] so you can grab the exact filtered URL (q, tag, sort). Commit: 19b845f (ops-deck-ui).
- Progress (2026-02-17 05:41 ET): Copy link now copies the full absolute URL (not just path), and if the clipboard API is blocked it falls back to a manual copy prompt. Commit: 4bcf06d (ops-deck-ui).
- Progress (2026-02-17 05:56 ET): Copy link button now has a proper focus-visible ring and an aria-label, so keyboard users can see where they are. Commit: dc1a1e6 (ops-deck-ui).
- Progress (2026-02-17 06:14 ET): Copy link button now disables briefly after copying and announces success via aria-live for screen readers. Commit: 8345b39 (ops-deck-ui).
- Progress (2026-02-17 06:36 ET): Search term highlighting now prefers the longer term when two matches start at the same position, so multi-word queries look less jittery. Commit: 7b3dc69 (ops-deck-ui).
- Progress (2026-02-17 06:48 ET): Added a /research/raw/[slug] route and a "Raw" link on the note page so you can open the original markdown in a new tab. Commit: f1c1ea5 (ops-deck-ui).
- Progress (2026-02-17 06:54 ET): Hardened /research/[slug] and /research/raw/[slug] against path traversal by validating slugs before reading from disk. Commit: 0748a81 (ops-deck-ui).
- Progress (2026-02-17 07:12 ET): Note page now shows the file updated time (mtime) under the title so you can tell how fresh the intel is at a glance. Commit: 067e9e4 (ops-deck-ui).
- Progress (2026-02-17 07:22 ET): Deduped note header parsing and slug validation into a shared helper to avoid drift between /research list, note view, and raw route. Commit: f31574e (ops-deck-ui).
- Progress (2026-02-17 07:39 ET): /research now reuses parsed query terms across highlighting and meta checks, shaving repeated parsing and keeping the render path calmer. Commit: 3dbdd83 (ops-deck-ui).
- Progress (2026-02-17 07:56 ET): Tag dropdown now sorts by usage count (descending) with alphabetical tie-break, so the most common tags sit at the top. Commit: d40ee5f (ops-deck-ui).

### 3) Ops Deck UI: Agent Activity receipts store
- Approved: design a receipts schema and build an Activity viewer.

### 6) VPS migration hardening plan
- Approved: draft a VPS migration plan and checklist.

## Completed
- None yet.
