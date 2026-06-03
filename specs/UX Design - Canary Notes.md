# UX Design — Canary Notes API

A headless JSON API; "UX" means response shapes and the operator status surface.
Kept deliberately small (build-plan fixture).

## Response conventions

- All responses are `application/json`.
- Errors: `{ "error": string }` with the appropriate status code.
- Success bodies echo the affected note.

## Surfaces

### S1 — Notes list (`GET /notes`)
A flat list of notes, each with a title and body preview. Creating a note calls
`POST /notes`.

### S2 — Note detail (`GET /notes/:id`)
A single note's full title + body, or a `404` empty state.

### S3 — Status surface (`GET /status`)
An operator status panel rendering the JSON from `GET /status`:

- `version` — deployed build version.
- `note_count` — number of stored notes.
- `brand_color` — the canary brand color, rendered as the panel accent.
  **The brand color is exactly `#2ec4b6`** (canary teal). This precise hex is
  load-bearing: it is the manual-AC token the e2e harness asserts in the PR body,
  so it must survive verbatim into the status response and the panel styling.

## Accessibility

- The status accent (`#2ec4b6`) must meet WCAG AA against its label text; pair it
  with `#08312c` text where used as a background fill.
