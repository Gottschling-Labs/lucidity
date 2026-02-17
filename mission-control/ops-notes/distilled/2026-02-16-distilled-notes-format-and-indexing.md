# Distilled notes format and indexing plan

Date: 2026-02-16
Tags: research, ops-deck, notes, indexing

## Goal

Make distilled notes easy to:
- list
- filter by tags
- full text search
- render as markdown

With no database and no cleverness. Just files.

## Proposed file conventions

Folder:
- `mission-control/ops-notes/distilled/`

File name:
- `YYYY-MM-DD-<kebab-topic>.md`

Header block at top of file:
- First line is an H1 title
- Then a small metadata block as simple `Key: value` lines

Example:

```
# Token, cost, and memory hygiene (OpenClaw field notes)

Date: 2026-02-16
Tags: research, cost, tokens, memory, ops

## What matters
...
```

Rules:
- `Date:` is ISO `YYYY-MM-DD`
- `Tags:` is a comma separated list
- keep tags lowercase, kebab where needed
- metadata lines must appear before the first `##` section

This stays readable in raw markdown and easy to parse.

## Indexing algorithm (boring on purpose)

At build time, crawl `distilled/*.md` and for each file:
- read the first ~50 lines
- parse `Date:` and `Tags:`
- derive slug from filename
- set `title` from the H1
- set `excerpt` from the first non empty paragraph after metadata

Store an index like:

```ts
type DistilledNote = {
  slug: string
  path: string
  title: string
  date: string
  tags: string[]
  excerpt?: string
}
```

## Rendering approach

Two layers:
1) List view uses the index only
2) Detail view reads the full markdown and renders it

Keep the renderer dumb. If a note needs special structure, write it in markdown.

## Open questions

1) YAML frontmatter
- nice, standard
- but it makes the file feel less like a field note

If we want it later, we can support both formats and migrate gradually.
