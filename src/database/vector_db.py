import json
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np

from src.config import Config


def chunk_text(text: str, chunk_size: int = Config.CHUNK_SIZE, overlap: int = 2) -> List[str]:
    chunks = []
    sentences = text.split('.')
    chunk = []
    
    for sentence in sentences:
        chunk.append(sentence)
        if len(chunk) >= 3 and len('.'.join(chunk)) > chunk_size:
            chunks.append('.'.join(chunk).strip() + '.')
            chunk = chunk[-overlap:]
    
    if chunk:
        chunks.append('.'.join(chunk))
    
    return chunks


class VectorDatabase:
    def __init__(self, contexts: str, save_file: Path, code_filepath: Path):
        self.contexts = contexts
        self.save_file = save_file
        self.code_info = pd.read_csv(code_filepath)
        self.model = SentenceTransformer(Config.EMBEDDING_MODEL)
        self.database: List[Dict[str, Any]] = []
    
    def create_database(self) -> None:
        chunks = chunk_text(self.contexts)
        embeddings = self._make_embeddings(chunks)
        
        self.database = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            self.database.append({
                "id": i,
                "context": chunk,
                "embedding": embedding.tolist()
            })
        
        self._add_code_examples(len(self.database))
        self._save_database()
    
    def _add_code_examples(self, start_id: int) -> None:
        col1, col2, _, _ = self.code_info.columns
        
        for i, (topic, desc) in enumerate(zip(self.code_info[col1], self.code_info[col2])):
            info = f"{topic}\n{desc}"
            embedding = self._make_embeddings([info])[0]
            self.database.append({
                "id": start_id + i,
                "context": info,
                "embedding": embedding.tolist()
            })
    
    def _make_embeddings(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts)
    
    def _save_database(self) -> None:
        with open(self.save_file, 'w') as f:
            json.dump(self.database, fp=f, indent=4)

