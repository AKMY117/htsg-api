# HT Speaker Geometry API (Render‑ready)

A minimal FastAPI service that returns a **Beginner Summary card** for your HT Speaker Geometry GPT. Startup is fast (no heavy deps). Swap in your full engine later.

## Endpoints
- `GET /health` → `{ "status": "ok" }`
- `GET /` → service info
- `HEAD /` → 200 (for Render’s probes)
- `GET /design` → `card` string

### Example
