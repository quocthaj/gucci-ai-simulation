import os
from dotenv import load_dotenv
load_dotenv()  # thêm dòng này lên đầu
import google.genai as genai
from groq import Groq

genai_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_gemini(system: str, history: list[dict], user_message: str) -> str:
    contents = []
    for m in history:
        contents.append({"role": m["role"], "parts": [{"text": m["content"]}]})
    contents.append({"role": "user", "parts": [{"text": user_message}]})

    response = genai_client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-3-flash-preview"),
        contents=contents,
        config={"system_instruction": system}
    )
    return response.text

def call_groq(prompt: str) -> str:
    response = groq_client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "llama3-8b-8192"),
        temperature=float(os.getenv("GROQ_TEMPERATURE", 0.0)),
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def llm_call(system: str, history: list[dict], user_message: str) -> str:
    """Public entry-point used by CHROAgent — routes to Gemini."""
    return call_gemini(system, history, user_message)