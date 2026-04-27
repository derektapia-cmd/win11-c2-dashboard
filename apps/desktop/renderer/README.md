# Renderer

This is the React + TypeScript dashboard interface.

## First Goal

The first renderer goal is a static local dashboard shell:

- Top command bar
- Side utility rail
- Tile grid
- Bottom crypto ticker placeholder
- Local-only placeholder data

No external APIs are called from this first version.

The dashboard does call the local backend health endpoint when it is running:

`http://127.0.0.1:8765/health`

It also uses the local Notes API:

`http://127.0.0.1:8765/notes`

The Quick Notes panel supports creating, pinning, editing, and deleting local notes.

The lock button toggles persisted Privacy Mode through:

`http://127.0.0.1:8765/settings`

The Compact button toggles a persisted denser dashboard layout through the same endpoint.

The Add Tile button opens tile visibility, ordering, and reset controls persisted through the same endpoint.

The Audit Log panel reads recent local actions from:

`http://127.0.0.1:8765/audit-log`

## Run

Optional `VITE_*` endpoint overrides are documented in the root `.env.example`.

```powershell
npm install
npm run dev
```

Then open the local Vite URL shown in the terminal.

To see live backend health, save notes, and persist dashboard settings, run the backend service first.
