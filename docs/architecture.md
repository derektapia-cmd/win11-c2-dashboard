# Architecture

This document captures the first approved shape of the Windows 11 command-center dashboard.

## Goal

Build a local-first desktop dashboard with an Electron shell, a React/TypeScript interface, and a Python FastAPI backend service.

## Boundaries

- The frontend owns layout, tiles, settings screens, and user interaction.
- The backend owns external API calls, token refresh, storage, scheduled sync work, and audit logging.
- Tiles communicate through shared contracts and approved event/data layers.
- One failing integration must not prevent the dashboard from opening.

## First Build Target

The first implementation target is a basic working skeleton:

- Repo and folder structure
- Backend health endpoint
- Frontend shell
- Tile registry
- Local-only notes/settings foundation
- No external API secrets required

