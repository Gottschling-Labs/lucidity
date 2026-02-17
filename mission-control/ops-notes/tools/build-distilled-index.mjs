#!/usr/bin/env node
/**
 * Build an index for mission-control/ops-notes/distilled/*.md
 *
 * Output: mission-control/ops-notes/distilled/index.json
 *
 * Intent: boring, readable, dependency-free.
 */

import fs from 'node:fs/promises'
import path from 'node:path'

const repoRoot = process.cwd()
const distilledDir = path.join(repoRoot, 'mission-control', 'ops-notes', 'distilled')
const outPath = path.join(distilledDir, 'index.json')

function toSlug(filename) {
  return filename.replace(/\.md$/i, '')
}

function parseNote(filePath, filename, content) {
  const lines = content.split(/\r?\n/)

  // title
  let title = null
  for (const line of lines.slice(0, 20)) {
    const m = line.match(/^#\s+(.+)\s*$/)
    if (m) {
      title = m[1].trim()
      break
    }
  }

  // metadata lives before the first ##
  const meta = {}
  for (const line of lines) {
    if (/^##\s+/.test(line)) break
    const m = line.match(/^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)\s*$/)
    if (m) meta[m[1]] = m[2]
  }

  const date = (meta.Date || '').trim()
  const tags = (meta.Tags || '')
    .split(',')
    .map((t) => t.trim())
    .filter(Boolean)

  // excerpt: first non-empty line after metadata, but before first ##
  let excerpt = ''
  let sawMeta = false
  for (const line of lines) {
    if (/^#\s+/.test(line)) continue
    if (/^[A-Za-z][A-Za-z0-9_-]*:/.test(line)) {
      sawMeta = true
      continue
    }
    if (/^##\s+/.test(line)) break

    if (!sawMeta) continue
    if (!line.trim()) continue

    excerpt = line.trim()
    break
  }

  return {
    slug: toSlug(filename),
    path: path.relative(repoRoot, filePath),
    title: title || toSlug(filename),
    date: date || filename.slice(0, 10),
    tags,
    excerpt: excerpt || undefined,
  }
}

async function main() {
  const entries = await fs.readdir(distilledDir, { withFileTypes: true })
  const mdFiles = entries
    .filter((e) => e.isFile())
    .map((e) => e.name)
    .filter((n) => n.toLowerCase().endsWith('.md'))
    .filter((n) => !['index.md'].includes(n.toLowerCase()))

  const notes = []
  for (const filename of mdFiles) {
    const filePath = path.join(distilledDir, filename)
    const content = await fs.readFile(filePath, 'utf8')
    notes.push(parseNote(filePath, filename, content))
  }

  // Sort newest first, then title for stability
  notes.sort((a, b) => {
    if (a.date !== b.date) return a.date < b.date ? 1 : -1
    return a.title.localeCompare(b.title)
  })

  const payload = {
    generatedAt: new Date().toISOString(),
    count: notes.length,
    notes,
  }

  await fs.writeFile(outPath, JSON.stringify(payload, null, 2) + '\n', 'utf8')
  process.stdout.write(`Wrote ${path.relative(repoRoot, outPath)} with ${notes.length} notes\n`)
}

main().catch((err) => {
  console.error(err)
  process.exitCode = 1
})
