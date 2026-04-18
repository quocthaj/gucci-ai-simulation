import os
from app.services.embedding import embed, cosine_similarity

class RAGService:
    def __init__(self, kb_dir: str):
        self.kb_dir = kb_dir
        self.documents = []  # List of {"path": str, "content": str, "embedding": list[float]}
        self._index_kb()

    def _index_kb(self):
        """Pre-embeds all text files in the knowledge base."""
        print(f"Indexing knowledge base in {self.kb_dir}...")
        for root, _, files in os.walk(self.kb_dir):
            for file in files:
                if file.endswith(".txt"):
                    path = os.path.join(root, file)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            content = f.read()
                            if not content.strip():
                                continue
                            self.documents.append({
                                "path": path,
                                "content": content,
                                "embedding": embed(content[:2000]) # Embed first chunk
                            })
                    except Exception as e:
                        print(f"Error indexing {path}: {e}")

    def retrieve_context(self, query: str, top_k: int = 1) -> str:
        """Retrieves most relevant content for a given query."""
        if not self.documents:
            return ""
        
        query_embedding = embed(query)
        results = []
        for doc in self.documents:
            sim = cosine_similarity(query_embedding, doc["embedding"])
            results.append((sim, doc["content"]))
        
        # Sort by similarity descending
        results.sort(key=lambda x: x[0], reverse=True)
        
        # Return top K results concatenated
        return "\n\n---\n\n".join([doc[1] for sim, doc in results[:top_k]])

# Singleton instance
kb_root = os.path.join(os.getcwd(), "data", "knowledge_base")
rag_service = RAGService(kb_root)
