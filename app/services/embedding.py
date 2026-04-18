# app/services/embedding.py

import os
from dotenv import load_dotenv
load_dotenv()

import numpy as np
from google import genai

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def embed(text: str) -> list[float]:
    response = client.models.embed_content(
        model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/gemini-embedding-2-preview"),
        contents=text
    )
    return response.embeddings[0].values

def cosine_similarity(a: list[float], b: list[float]) -> float:
    a, b = np.array(a), np.array(b)
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))