from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import fitz

from app.core.config import settings
from app.utils.chunking import chunk_text


class ResumeService:
    def __init__(self) -> None:
        self.base_dir = Path(settings.storage_dir)
        self.resume_dir = self.base_dir / "resumes"
        self.resume_dir.mkdir(parents=True, exist_ok=True)

    def extract_text_from_pdf(self, file_path: Path) -> str:
        document = fitz.open(file_path)
        text = []
        for page in document:
            text.append(page.get_text())
        return "\n".join(text).strip()

    def save_resume(self, user_id: str, filename: str, file_bytes: bytes) -> Path:
        user_dir = self.resume_dir / user_id
        user_dir.mkdir(parents=True, exist_ok=True)
        file_path = user_dir / f"{uuid4().hex}_{filename}"
        file_path.write_bytes(file_bytes)
        return file_path

    def chunk_resume(self, text: str) -> list[str]:
        return chunk_text(text)


resume_service = ResumeService()
