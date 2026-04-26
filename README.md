# win11-c2-dashboard

Windows 11 command-center dashboard for a personal desktop cockpit: local notes, settings, real-time tiles, market data, AI launch points, terminal access, and future wallet/email integrations.

## Current Phase

Foundation setup.

The repo currently contains the roadmap, starter documentation, and the planned folder structure. The first implementation target is a basic working skeleton before adding external services or secrets.

## Planned Stack

- Electron desktop shell
- React + TypeScript renderer
- Python FastAPI backend
- SQLite local database

## Project Rules

- Keep secrets out of Git.
- Start local-only before connecting external APIs.
- Each tile should fail independently without breaking the full dashboard.
- Wallet private keys and seed phrases are never stored by this app.

## Docs

- [Roadmap](docs/roadmap.md)
- [Architecture](docs/architecture.md)
- [API Integrations](docs/api-integrations.md)
- [Security Model](docs/security-model.md)
- [Tile Specs](docs/tile-specs.md)
- [Launch Checklist](docs/launch-checklist.md)
