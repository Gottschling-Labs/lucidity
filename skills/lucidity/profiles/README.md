# Lucidity profiles (draft)

Profiles are an **advisory layer** for adapting Lucidity to different runtime and retrieval constraints.

They are intentionally lightweight for now.

## Why profiles exist

Different companion runtimes have different constraints:
- context window size
- latency tolerance
- local vs hosted models
- how much retrieval noise they can tolerate
- whether they should bias toward compact summaries or broader recall

Lucidity profiles let us describe those constraints without baking them into the memory corpus itself.

## Current status

These examples are **reference presets**, not a hard API.

They should be treated as:
- documentation
- implementation guidance
- future inputs for installer/config UX

## Included example profiles

- `openclaw-default.json` - balanced default for a normal OpenClaw deployment
- `llama-local-8k.json` - tighter retrieval posture for smaller local context windows
- `offline-voice-low-latency.json` - aggressively compact retrieval for low-latency/offline use

## Conceptual fields

- `runtimeProfileId`: human-readable profile id
- `retrievalProfile`: retrieval posture name
- `maxSnippets`: soft cap for injected memory snippets
- `preferCurated`: whether to bias toward curated memory first
- `topicBriefBias`: whether to prefer topic briefs over raw daily logs
- `latencyBias`: trade recall breadth for speed when needed
- `notes`: explanatory intent for humans

## Important note

Profiles should influence **retrieval behavior and defaults**, not redefine the source-of-truth memory model.

Lucidity still treats the Markdown workspace as canonical.
