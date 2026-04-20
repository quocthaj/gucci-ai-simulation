# Gucci AI Simulation — CHRO NPC Engine

> **AI Co-Worker Engine** cho Edtronaut Job Simulation Platform.  
> Mô phỏng buổi làm việc 1-on-1 với CHRO của Gucci Group — nhân vật NPC được thúc đẩy bởi **Dual-Engine AI** (Groq Llama 70B + Groq Llama 8B).

The prototype is deployed on Render. You can interact with the API directly via the interactive Swagger UI:

- 🔗 **Demo:** [Click here to test the web](https://gucci-chro-agent.onrender.com)
- *(Note: Hosted on a free Render tier — server may sleep after 15 minutes of inactivity. Allow ~30-50 seconds for cold start on first request.)*

---

## Architecture — Dual-Engine Native SDK

```
User ──► FastAPI /chat
              │
              ├──► SupervisorAgent (Groq llama-3.1-8b-instant)
              │       • Single-call 3-in-1 analysis:
              │           - Intent classification (high/low)
              │           - Stagnation detection
              │           - Rapport delta scoring
              │       • Self-correction: verify_response_quality()
              │       • Dynamic injection when user is stuck (≥3 turns)
              │
              └──► CHROAgent (Groq llama-3.3-70b-versatile)
                      • Custom SlidingWindowMemory (k=6, no LangChain Memory)
                      • RAG: Google  + cosine similarity
                      • Safety flag detection (comp_band_restricted, etc.)
                      • Persona: Gucci CHRO — warm, strategic, never breaks character
```

| Layer | Model | Role |
|---|---|---|
| **Main Agent Brain** | `groq/llama-3.3-70b-versatile` | Generates CHRO persona responses |
| **Supervisor** | `groq/llama-3.1-8b-instant` | Intent, stagnation, rapport, quality check |
| **Embeddings** | `google/gemini-embedding-2-preview` | RAG knowledge base indexing & retrieval |

---

## Key Features

| Feature | Description |
|---|---|
| 🎭 **Ironclad Persona** | CHRO never breaks character — rejects off-topic, AI disclosure attempts, prompt injections |
| 🧠 **Optimized Supervisor** | Single Groq call = 3-in-1 analysis (intent + stagnation + rapport) for low latency |
| 🔁 **Self-Correction Loop** | Supervisor critiques CHRO response; agent auto-rewrites if quality check fails |
| 💉 **Dynamic Injection** | After 3 stagnant turns, Supervisor injects a covert steering hint to the CHRO prompt |
| 📚 **RAG Pipeline** | Knowledge base (`data/knowledge_base/`) pre-embedded at startup; top-1 context injected per turn |
| 💾 **Persistent Sessions** | Session state saved to `sessions_dev.json` — survives server restarts |
| 🛡️ **Safety Flags** | Detects restricted topics (e.g., salary bands) and returns `safety_flags` in API response |
| 🌐 **Bilingual** | Auto-detects user language — responds in Vietnamese or English accordingly |
| 📊 **React Frontend** | Live state panel showing rapport score, competencies covered, stagnation counter |

---

## Competency Tracking

The agent tracks which of Gucci's 4 core leadership competencies the user has discussed:

| Competency | Keywords detected |
|---|---|
| **Vision** | vision, tầm nhìn, strategic, chiến lược, direction |
| **Entrepreneurship** | entrepreneurship, tinh thần doanh chủ, innovation, risk |
| **Passion** | passion, đam mê, commitment, enthusiasm |
| **Trust** | trust, tin tưởng, transparency, integrity |

Competencies are tracked from **user messages only** (not AI responses) to reflect genuine understanding.

---

## Project Structure

```
gucci-ai-simulation/
├── app/
│   ├── main.py                  # FastAPI entrypoint — /chat endpoint, session persistence
│   ├── core/
│   │   ├── agent.py             # CHROAgent — persona logic, self-correction, RAG integration
│   │   │                        # SlidingWindowMemory — custom k=6 window (no LangChain Memory)
│   │   ├── supervisor.py        # SupervisorAgent — 3-in-1 analysis, quality verification, injection
│   │   └── schema.py            # Pydantic data models (NPCResponse, StateUpdate, CompetencyFlag)
│   └── services/
│       ├── llm_service.py       # Gemini + Groq SDK clients (llm_call → call_groq_chat)
│       ├── rag_service.py       # RAGService — index KB at startup, cosine similarity retrieval
│       └── embedding.py         # Google gemini-embedding-2-preview wrapper
├── data/
│   └── knowledge_base/          # .txt files auto-indexed by RAGService on startup
├── fe/                          # React + Vite frontend (npm run dev → localhost:5173)
│   └── src/
│       ├── App.jsx              # Layout: ChatWindow (70%) + StatePanel (30%)
│       └── assets/components/
│           ├── ChatWindow.jsx   # Chat UI — sends to /chat, displays safety flags
│           └── StatePanel.jsx   # Live session state dashboard
├── sessions_dev.json            # Persistent session store (auto-generated, gitignored)
├── .env.example                 # Environment variable template
├── requirements.txt
└── README.md
```

---

## Setup & Run Locally

```bash
# 1. Clone repo
git clone https://github.com/quocthaj/gucci-ai-simulation
cd gucci-ai-simulation

# 2. Create & activate virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
copy .env.example .env
# Edit .env — fill in GOOGLE_API_KEY and GROQ_API_KEY

# 5. Run backend
uvicorn app.main:app --reload --port 8000

# 6. Run frontend (separate terminal)
cd fe
npm install
npm run dev
# → http://localhost:5173
```

### Environment Variables

| Variable | Description |
|---|---|
| `GOOGLE_API_KEY` | Google AI Studio API key (for embeddings) |
| `GROQ_API_KEY` | Groq API key (for main agent + supervisor) |
| `GEMINI_MODEL` | Gemini model name (fallback — default: `gemini-3-flash-preview`) |
| `GROQ_MODEL` | Groq model for supervisor (default: `llama-3.1-8b-instant`) |
| `GROQ_CHAT_MODEL` | Groq model for main agent (default: `llama-3.3-70b-versatile`) |
| `GROQ_TEMPERATURE` | Supervisor temperature (default: `0.0`) |
| `GOOGLE_EMBEDDING_MODEL` | Embedding model (default: `models/gemini-embedding-2-preview`) |

---

## API Reference
**Demo:** [Click here to test the API](https://gucci-chro-agent.onrender.com/docs)
### `POST /chat`

**Request:**
```json
{
  "session_id": "user_001",
  "persona_id": "chro",
  "user_message": "Tôi muốn thiết kế chương trình 360 feedback cho các lãnh đạo"
}
```

**Response:**
```json
{
  "message": "Một sáng kiến đúng hướng. Nhưng trước khi thiết kế công cụ, tôi cần hiểu: ai là người thụ hưởng thực sự? Và bằng cách nào bạn đảm bảo phản hồi đó thúc đẩy Vision thay vì chỉ đánh giá hiệu suất?",
  "state": {
    "stagnation_counter": 0,
    "rapport_score": 0.55,
    "competencies_covered": ["Vision"],
    "injection_fired": false
  },
  "safety_flags": []
}
```

**Safety flags:** `comp_band_restricted` — triggered when user asks about salary bands / compensation ranges.

---

## Deployment (Render) — Single Service Full-Stack

FastAPI serves **both** the API and the React frontend as static files from `fe/dist/`.
No separate frontend hosting needed.

```
Render Web Service
├── POST /chat          → CHROAgent (FastAPI)
├── GET  /docs          → Swagger UI
└── GET  /              → React SPA (fe/dist/index.html)
    └── GET /assets/*   → JS, CSS bundles
```

**Build command** (installs Python deps + builds React):
```bash
pip install -r requirements.txt && cd fe && npm install && npm run build
```

**Start command:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Set the following **Environment Variables** in Render dashboard:
- `GOOGLE_API_KEY`
- `GROQ_API_KEY`
- `GROQ_CHAT_MODEL=llama-3.3-70b-versatile`
- `GROQ_MODEL=llama-3.1-8b-instant`
- `GROQ_TEMPERATURE=0.0`
- `GOOGLE_EMBEDDING_MODEL=models/gemini-embedding-2-preview`

> ⚠️ `sessions_dev.json` is ephemeral on Render's free tier — sessions reset on each deploy. For persistence, upgrade to a paid instance or integrate a Redis/PostgreSQL store.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Uvicorn |
| Main LLM | Groq `llama-3.3-70b-versatile` (Native SDK) |
| Supervisor LLM | Groq `llama-3.1-8b-instant` (Native SDK) |
| Embeddings | Google `gemini-embedding-2-preview` (Native SDK) |
| Memory | Custom `SlidingWindowMemory` (no LangChain) |
| Frontend | React + Vite |
| Deployment | Render (free tier) |
