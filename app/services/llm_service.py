import os
import json
from dotenv import load_dotenv
load_dotenv() 

import google.genai as genai
from groq import Groq

genai_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_gemini(system: str, history: list[dict], user_message: str) -> str:
    """Gemini call for RAG or specific tasks if quota permits."""
    contents = []
    for m in history:
        contents.append({"role": m["role"], "parts": [{"text": m["content"]}]})
    contents.append({"role": "user", "parts": [{"text": user_message}]})

    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip()
    
    response = genai_client.models.generate_content(
        model=model_name,
        contents=contents,
        config={"system_instruction": system}
    )
    return response.text

def call_groq(prompt: str) -> str:
    """Simple 1-shot Groq call for classification."""
    response = groq_client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        temperature=float(os.getenv("GROQ_TEMPERATURE", 0.0)),
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def call_groq_chat(system: str, history: list[dict], user_message: str) -> str:
    """Full chat call for main Agent brain using high-quality Llama model."""
    messages = [{"role": "system", "content": system}]
    for m in history:
        messages.append({"role": m["role"], "content": m["content"]})
    messages.append({"role": "user", "content": user_message})

    # Default to 70B for the main agent brain
    model_name = os.getenv("GROQ_CHAT_MODEL", "llama-3.3-70b-versatile")

    response = groq_client.chat.completions.create(
        model=model_name,
        temperature=0.7,
        messages=messages,
        max_tokens=2048
    )
    return response.choices[0].message.content

def llm_call(system: str, history: list[dict], user_message: str) -> str:
    """Public entry-point used by CHROAgent — defaulting to Groq for stable quota."""
    return call_groq_chat(system, history, user_message)