from __future__ import annotations

from typing import Iterable


def chunk_text(text: str, chunk_size: int = 700, overlap: int = 120) -> list[str]:
    words = text.split()
    if not words:
        return []
    chunks: list[str] = []
    step = max(1, chunk_size - overlap)
    for start in range(0, len(words), step):
        chunk = words[start : start + chunk_size]
        if chunk:
            chunks.append(" ".join(chunk))
    return chunks
