from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer

from src.config import Config


class Retriever:
    def __init__(self, contexts: List[Dict[str, Any]]):
        self.contexts = contexts
        self.model = SentenceTransformer(Config.EMBEDDING_MODEL)
    
    def search(self, query: str, top_k: int = Config.TOP_K) -> str:
        query_embedding = self.model.encode(query)
        scores = []
        
        for context in self.contexts:
            context_id = context['id']
            context_embedding = np.array(context['embedding'])
            similarity_score = self._compute_cosine_similarity(query_embedding, context_embedding)
            scores.append([context_id, similarity_score])
        
        scores.sort(key=lambda x: x[1], reverse=True)
        
        retrieved_contexts = []
        for i in range(min(top_k, len(scores))):
            context_id, _ = scores[i]
            retrieved_contexts.append(self.contexts[context_id]['context'])
        
        return '\n'.join(retrieved_contexts)
    
    def build_prompt(self, query: str, top_k: int = Config.TOP_K) -> str:
        retrieved_context = self.search(query, top_k)
        return f"{retrieved_context}\n{query}"
    
    @staticmethod
    def _compute_cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        vec2 = np.squeeze(vec2)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

