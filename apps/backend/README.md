# Backend

This is the local Python service for the Windows 11 command-center dashboard.

## What It Does First

The first backend goal is intentionally small:

- Start a FastAPI app.
- Answer `GET /health`.
- Save, list, pin, edit, and delete local notes with SQLite.
- Persist dashboard settings such as Privacy Mode and Compact Mode with SQLite.
- Give the future Electron/React app a local service to talk to.

## Setup

From the project root:

```powershell
cd apps\backend
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

For local test tools:

```powershell
.\.venv\Scripts\python -m pip install -r requirements-dev.txt
```

## Run

Optional local overrides are documented in the root `.env.example`. Set them in the shell before starting the backend if you need to move the SQLite database or allowed renderer origins.

```powershell
.\.venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8765 --reload
```

Then open:

- Health check: `http://127.0.0.1:8765/health`
- Notes API: `http://127.0.0.1:8765/notes`
- Settings API: `http://127.0.0.1:8765/settings`
- API docs: `http://127.0.0.1:8765/docs`

## Beginner Checkpoint

If `/health` returns `status: ok`, the backend skeleton is alive.

The React renderer is allowed to call this local backend from:

- `http://127.0.0.1:5173`
- `http://localhost:5173`

## Test

```powershell
.\.venv\Scripts\python -m pytest
```
