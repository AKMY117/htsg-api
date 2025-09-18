from fastapi import FastAPI, HTTPException, Query, Response
app = FastAPI(title="HT Speaker Geometry API", version="0.2.0")

# Allow calls from ChatGPT, localhost, etc.
app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

class DesignResponse(BaseModel):
card: str

class Health(BaseModel):
status: str = "ok"

@app.get("/health", response_model=Health)
def health():
return Health()

@app.get("/", include_in_schema=False)
def root():
return {
"service": "HTSG API",
"docs": "/docs",
"openapi": "/openapi.json",
"try": "/design?room=430x300x260%20cm&layout=7.x.4&ear_cm=120&fru=true",
}

# Silence Render’s HEAD probe 405s
@app.head("/", include_in_schema=False)
def head_root():
return Response(status_code=200)

@app.get("/design", response_model=DesignResponse)
def design_endpoint(
room: str = Query(..., description="Room dims, e.g. '430x300x260 cm' or '12x14x9 ft'"),
layout: str = Query(..., description="One of 5.x.2, 5.x.4, 5.x.6, 7.x.2, 7.x.4, 7.x.6", example="7.x.4"),
ear_cm: float = Query(120.0, ge=60, le=180, description="Ear height in cm"),
fru: bool = Query(False, description="Compute FRU (Seat-Adjust) card as well"),
notes: Optional[str] = Query(None, description="Optional notes to include in card")
):
# Parse & validate inputs
room_cm = parse_room_dimensions(room)
if not room_cm:
raise HTTPException(status_code=422, detail="Could not parse room dimensions. Use LxWxH with units.")

if not validate_layout(layout):
raise HTTPException(status_code=422, detail="layout must be one of 5.x.2, 5.x.4, 5.x.6, 7.x.2, 7.x.4, 7.x.6")

# Build response card (Dolby Reference + optional FRU mini-card)
try:
card = build_card(room_cm, layout, ear_cm, fru=fru, extra_notes=notes)
except ValueError as e:
raise HTTPException(status_code=422, detail=str(e))
except Exception as e:
raise HTTPException(status_code=500, detail=f"Internal error: {e}")

return DesignResponse(card=card)
