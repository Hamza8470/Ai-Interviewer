from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import FileResponse

from app.core.dependencies import get_current_user
from app.services.speech_service import speech_service
from app.utils.serializers import serialize_doc

router = APIRouter()


@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    temp_dir = Path(speech_service.base_dir) / "uploads"
    temp_dir.mkdir(parents=True, exist_ok=True)
    audio_path = temp_dir / f"{uuid4().hex}_{file.filename}"
    audio_path.write_bytes(await file.read())
    transcript = speech_service.transcribe(audio_path)
    return {"transcript": transcript, "file_path": str(audio_path)}


@router.post("/tts")
async def text_to_speech(text: str = Form(...), current_user: dict = Depends(get_current_user)):
    output_path = speech_service.text_to_speech(text, uuid4().hex)
    return FileResponse(str(output_path), media_type="audio/mpeg", filename=output_path.name)
