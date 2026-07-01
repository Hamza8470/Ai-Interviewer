from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.core.config import settings


class RAGService:
    def __init__(self) -> None:
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.base_dir = Path(settings.storage_dir) / "faiss"
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _paths(self, resume_id: str) -> tuple[Path, Path]:
        return self.base_dir / f"{resume_id}.index", self.base_dir / f"{resume_id}.json"

    def build_index(self, resume_id: str, chunks: list[str]) -> dict[str, Any]:
        if not chunks:
            return {"chunks": [], "index_built": False}
        embeddings = self.model.encode(chunks, normalize_embeddings=True)
        embeddings = np.asarray(embeddings, dtype="float32")
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)
        index.add(embeddings)
        index_path, meta_path = self._paths(resume_id)
        faiss.write_index(index, str(index_path))
        meta_path.write_text(json.dumps({"chunks": chunks}, ensure_ascii=False), encoding="utf-8")
        return {"chunks": chunks, "index_built": True}

    def load_index(self, resume_id: str) -> tuple[Any, list[str]]:
        index_path, meta_path = self._paths(resume_id)
        if not index_path.exists() or not meta_path.exists():
            raise FileNotFoundError("RAG index not found")
        index = faiss.read_index(str(index_path))
        metadata = json.loads(meta_path.read_text(encoding="utf-8"))
        return index, metadata.get("chunks", [])

    def retrieve(self, resume_id: str, query: str, top_k: int = 3) -> list[dict[str, Any]]:
        index, chunks = self.load_index(resume_id)
        query_embedding = self.model.encode([query], normalize_embeddings=True)
        query_embedding = np.asarray(query_embedding, dtype="float32")
        scores, indices = index.search(query_embedding, top_k)
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(chunks):
                continue
            results.append({"chunk": chunks[idx], "score": float(score)})
        return results


rag_service = RAGService()
