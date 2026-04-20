import json
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.core.agent import CHROAgent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
SESSION_FILE = "sessions_dev.json"

# ── Static files (React build) ──────────────────────────────────────────────
DIST_DIR = Path(__file__).parent.parent / "fe" / "dist"

def load_all_sessions():
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {sid: CHROAgent.from_dict(sdata) for sid, sdata in data.items()}
        except Exception as e:
            print(f"Error loading sessions: {e}")
    return {}

def save_all_sessions(sessions_dict):
    try:
        data = {sid: agent.to_dict() for sid, agent in sessions_dict.items()}
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving sessions: {e}")

# Load initial sessions
sessions: dict[str, CHROAgent] = load_all_sessions()

# CORS — allow localhost for dev; on Render both FE and BE are same origin so not needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    session_id: str
    persona_id: str
    user_message: str

@app.post("/chat")
def chat(req: ChatRequest):
    if req.session_id not in sessions:
        sessions[req.session_id] = CHROAgent(
            persona_id=req.persona_id,
            session_id=req.session_id
        )
    agent = sessions[req.session_id]
    result = agent.run(req.user_message)

    # Save after each interaction to persist state
    save_all_sessions(sessions)

    return {
        "message": result.assistant_message,
        "state": {
            "stagnation_counter": result.state_update.stagnation_counter,
            "rapport_score": result.state_update.rapport_score,
            "competencies_covered": [
                c.value for c in result.state_update.competencies_covered
            ],
            "injection_fired": result.state_update.injection_fired,
        },
        "safety_flags": result.safety_flags
    }

# ── Serve React SPA (must come AFTER API routes) ────────────────────────────
if DIST_DIR.exists():
    # Serve static assets (JS, CSS, images)
    app.mount("/assets", StaticFiles(directory=DIST_DIR / "assets"), name="assets")

    @app.get("/favicon.svg")
    def favicon():
        return FileResponse(DIST_DIR / "favicon.svg")

    # Catch-all: serve index.html for any non-API route (SPA fallback)
    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        index = DIST_DIR / "index.html"
        if index.exists():
            return FileResponse(index)
        return {"message": "Frontend not built. Run: cd fe && npm run build"}
else:
    @app.get("/")
    def root():
        return {
            "message": "Gucci CHRO Agent API is running.",
            "note": "Frontend not built. Run: cd fe && npm run build",
            "docs": "/docs"
        }