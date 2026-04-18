# Gucci AI Simulation — CHRO NPC Engine

AI Co-Worker Engine cho Edtronaut Job Simulation Platform.
Demo: Gucci Group CHRO NPC powered by Gemini 3 Flash + Groq Llama3.

## Architecture

- **Main Persona Agent**: Gemini 3 Flash Preview (1M context)
- **Supervisor Agent**: Groq Llama3 8B (ultra-low latency)
- **Framework**: FastAPI + LangChain Memory

## Setup

```bash
# 1. Clone repo
git clone https://github.com/yourname/gucci-ai-simulation
cd gucci-ai-simulation

# 2. Tạo virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Cài thư viện
pip install -r requirements.txt

# 4. Tạo file .env
copy .env.example .env
# Điền API key vào .env

# 5. Chạy server
uvicorn app.main:app --reload --port 8000
```

## Test API

Mở browser: `http://127.0.0.1:8000/docs`

Hoặc dùng curl:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"test_001\", \"persona_id\": \"chro\", \"user_message\": \"Tôi muốn thiết kế chương trình 360 feedback\"}"
```

## Sample Response

```json
{
  "message": "Một sáng kiến đúng hướng...",
  "state": {
    "stagnation_counter": 0,
    "rapport_score": 0.5,
    "competencies_covered": [],
    "injection_fired": false
  },
  "safety_flags": [],
  "token_usage": {
    "prompt_tokens": 312,
    "response_tokens": 198,
    "total_tokens": 510
  }
}
```

## Project Structure

```
gucci-ai-simulation/
├── app/
│   ├── main.py              # FastAPI entrypoint
│   ├── core/
│   │   ├── agent.py         # CHROAgent — main NPC logic
│   │   ├── supervisor.py    # SupervisorAgent — Director layer
│   │   └── schema.py        # Data models
│   └── services/
│       ├── llm_service.py   # Gemini + Groq clients
│       └── embedding.py     # Google Embedding + cosine similarity
├── data/knowledge_base/     # Gucci HR documents for RAG
├── .env.example
├── requirements.txt
└── README.md
```

## Key Features

- CHRO persona giữ đúng vai trong mọi tình huống
- Supervisor Agent phát hiện user bị stuck sau 3 turns
- Dynamic prompt injection — hint tự nhiên không lộ ra ngoài
- Token usage tracking mỗi turn
- Tự động detect ngôn ngữ — trả lời tiếng Việt hoặc tiếng Anh