# app.py
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import re

app = FastAPI(title="HT Speaker Geometry API", version="0.1.0")

class DesignResponse(BaseModel):
    card: str

# --- TEMP: minimal local implementation so the service can start on Render ---
# Replace this with your real geometry engine when ready.
def design(room_str: str, layout: str, ear_cm: float, want_fru: bool):
    # Very light validation; your real code can parse/compute here.
    if not re.match(r"^(5|7)\.x\.(2|4|6)$", layout):
        raise ValueError("layout must be one of 5.x.2, 5.x.4, 5.x.6, 7.x.2, 7.x.4, 7.x.6")
    card = (
        f"Layout: {layout}\n"
        f"Room: {room_str}\n"
        f"Ear height: {ear_cm:.1f} cm\n"
        f"FRU: {'on' if want_fru else 'off'}\n"
        "Result: (stub) Dolby Reference computed. FRU alt available."
    )
    return {"card": card}
# ---------------------------------------------------------------------------

@app.get("/design", response_model=DesignResponse)
def design_endpoint(
    room: str = Query(..., description="e.g. '430x300x260 cm'"),
    layout: str = Query(..., description="One of 5.x.2, 5.x.4, 5.x.6, 7.x.2, 7.x.4, 7.x.6", example="7.x.4"),
    ear_cm: float = 120.0,
    fru: bool = False,
):
    try:
        res = design(room_str=room, layout=layout, ear_cm=ear_cm, want_fru=fru)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    card = res.get("card") if isinstance(res, dict) else str(res)
    return {"card": card}

@app.get("/", include_in_schema=False)
def root():
    return {
        "ok": True,
        "try": "/design?room=430x300x260%20cm&layout=7.x.4&ear_cm=120&fru=true",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }
