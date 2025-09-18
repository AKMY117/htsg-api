from fastapi import FastAPI, Query
from pydantic import BaseModel
from your_module import design # ✅ change to your real module

app = FastAPI(title="HT Speaker Geometry API", version="0.1.0")

class DesignResponse(BaseModel):
card: str

@app.get("/design", response_model=DesignResponse)
def design_endpoint(
room: str = Query(..., description="e.g. '430x300x260 cm'"),
layout: str = Query(..., pattern=r"^(5|7)\.x\.(2|4|6)$", example="7.x.4"),
ear_cm: float = 120.0,
fru: bool = False,
):
res = design(room_str=room, layout=layout, ear_cm=ear_cm, want_fru=fru)
# If `res` is a dict, adapt accordingly. We only need a string card.
card = res.get("card") if isinstance(res, dict) else str(res)
return {"card": card}

@app.get("/")
def root():
return {"ok": True, "try": "/design?room=430x300x260%20cm&layout=7.x.4&ear_cm=120&fru=true"}