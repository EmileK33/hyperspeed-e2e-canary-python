# User Stories — Canary Notes API

A tiny Python notes HTTP API (Poetry + pytest). A build-plan **fixture**
(issue #40 / #143) shaped to decompose into 5 sessions across 3 phases (Phase 0
integration harness + 2 feature phases) with disjoint file ownership. No
database — an in-memory store keeps the fixture cheap.

## Epic 1 — Data layer

### US-001 — Note models
**As a** developer **I want** typed note models **so that** the store and routes
share one shape.

- AC-1: A `Note` dataclass (`id: str`, `title: str`, `body: str`) is exported
  from `app/models.py`.
- AC-2: A `new_note(title, body)` factory assigns a stable id.

### US-002 — In-memory note store
**As a** developer **I want** a store module **so that** routes persist notes
without embedding storage details.

- AC-1: `add`, `get`, `list_all` are exported from `app/store.py` and operate on
  `Note` values.
- AC-2: An integration test adds a note and reads it back.

## Epic 2 — Routes

### US-003 — Create + list notes
**As a** user **I want** to create and list notes **so that** I can capture
thoughts.

- AC-1: `POST /notes` creates a note and returns `201` with the created note.
- AC-2: `GET /notes` returns all notes as JSON.

### US-004 — Read a note
**As a** user **I want** to read one note **so that** I can review it.

- AC-1: `GET /notes/:id` returns the note or `404`.

### US-005 — Status surface
**As an** operator **I want** a status route **so that** I can see build + brand
metadata.

- AC-1: `GET /status` returns `200` with a JSON status body.
- AC-2: The body includes `version` and `note_count`.
- AC-3 **[MANUAL]**: The status JSON includes the canary brand color
  `#2ec4b6` in a `brand_color` field. *(Human sign-off required — verify the
  exact teal hex renders in the response and matches the brand guideline.)*
