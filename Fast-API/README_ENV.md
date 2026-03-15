# Environment variables (local dev)

This file explains how to use the environment variables for the Fast-API app.

Files
- `.env.example`: example values you can copy to `.env`.
- `.env`: local environment loaded by `pydantic.BaseSettings` in `config.py`.

Available variables
- `APP_NAME` — application name (used in logs, metadata).
- `DEBUG` — `true` or `false` (enables debug behavior where applicable).
- `HOST` — host interface to bind the server (default `127.0.0.1`).
- `PORT` — port to run the server on (default `8000`).
- `RESERVATION_MIN_HOURS` — integer, minimum hours in advance a reservation must be made.

Quick start (development)
1. Copy example env:

```bash
cd Fast-API
cp .env.example .env
```

2. Install requirements (if not already):

```bash
python -m pip install -r requirements.txt
```

3. Run the app with `uvicorn` (loads `.env` via `config.py`):

```bash
cd Fast-API
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Notes
- `config.py` uses `pydantic.BaseSettings` and reads `.env` by default. Change values in `.env` for local overrides.
- Tests use the running server; ensure the app is running before executing `Fast-API/tests/run_tests.py`.
