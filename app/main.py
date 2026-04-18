from fastapi import FastAPI
from pydantic import BaseModel
from app.core.agent import CHROAgent

app = FastAPI()
sessions: dict[str, CHROAgent] = {}

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