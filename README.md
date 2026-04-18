# Gucci AI Simulation — CHRO NPC Engine

AI Co-Worker Engine cho Edtronaut Job Simulation Platform.
Demo: Gucci Group CHRO NPC powered by Gemini 3 Flash + Groq Llama3.
The prototype is deployed on Render. You can interact with the API directly via the interactive Swagger UI:
* **Swagger UI / API Docs:** [👉 Click here to test the API](https://gucci-chro-agent.onrender.com/docs)
* *(Note: As this is hosted on a free Render tier, the server may sleep after 15 minutes of inactivity. Please allow ~30-50 seconds for the initial "cold start" upon your first request).*

## Architecture: Native SDK Dual-Engine

Hệ thống sử dụng kiến trúc **Dual-Engine** tối ưu hóa cho độ trễ và khả năng đóng vai (persona maintenance):

- **Main Persona Agent (Engine 1)**: Gemini 3 Flash Preview (1M context) chịu trách nhiệm sinh nội dung, đóng vai CHRO và xử lý tri thức chuyên sâu.
- **Supervisor Agent (Engine 2)**: Groq Llama3 8B (ultra-low latency) đóng vai trò "Director" ngầm:
    - **Semantic Router**: Phân loại Intent (Low vs High) để quyết định luồng xử lý.
    - **Stagnation Detection**: Theo dõi mức độ lặp lại của User.
    - **Rapport Scoring**: Đánh giá nồng độ tin cậy và thái độ của User.

### Advanced Optimization Layers
1. **Semantic Router**: Tự động chuyển hướng câu hỏi đơn giản (chào hỏi, cảm ơn) vào bộ quy tắc **Short-circuit Cache** để phản hồi <100ms.
2. **RAG Pipeline**: Tự động tìm kiếm tài liệu từ Knowledge Base dựa trên độ tương đồng ngữ nghĩa (Cosine Similarity) trước khi gửi context cho Gemini.
3. **Smart Control**: Tự động "tiêm" (inject) kịch bản định hướng nếu User bị kẹt (stuck) sau 3 lượt hội thoại.

## Setup

```bash
# 1. Clone repo
git clone https://github.com/quocthaj/gucci-ai-simulation
cd gucci-ai-simulation

# 2. Tạo virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Cài thư viện (Native SDKs + core requirements)
pip install -r requirements.txt

# 4. Tạo file .env
copy .env.example .env
# Điền API key vào .env
```

## Test API

Mở browser: `http://127.0.0.1:8000/docs`

Hoặc dùng curl:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"test_001\", \"persona_id\": \"chro\", \"user_message\": \"Chào ông\"}"
```

## Project Structure

```
gucci-ai-simulation/
├── app/
│   ├── main.py              # FastAPI entrypoint
│   ├── core/
│   │   ├── agent.py         # CHROAgent logic — Router & Cache integration
│   │   ├── supervisor.py    # SupervisorAgent — Groq Director layer
│   │   └── schema.py        # Pydantic & Data models
│   └── services/
│       ├── llm_service.py   # Native SDK clients (Gemini + Groq)
│       ├── rag_service.py   # RAG Engine — Indexing & Retrieval
│       └── embedding.py     # Google Embedding API handler
├── data/knowledge_base/     # Tài liệu Gucci HR (Vector source)
├── .env.example
├── requirements.txt
└── README.md
```

## Key Features

- **Persona Integrity**: CHRO giữ đúng mandate, không cầm tay chỉ việc, bảo vệ DNA thương hiệu.
- **Short-circuit Response**: Phản hồi tức thì cho Low Intent, tiết kiệm 100% chi phí gọi LLM lớn.
- **Knowledge-Aware**: Tự động tra cứu framework năng lực từ file vật lý thông qua RAG.
- **Dynamic Guidance**: Supervisor Agent can thiệp bằng "invisible prompts" để điều hướng hội thoại.
- **Multilingual Native**: Tự động nhận diện và phản hồi theo ngôn ngữ của User (Việt/Anh).
