from __future__ import annotations

from io import BytesIO
from pathlib import Path

from gtts import gTTS

from app.core.config import settings

try:
    import whisper
except Exception:  # pragma: no cover - optional dependency fallback
    whisper = None


class SpeechService:
    def __init__(self) -> None:
        self.base_dir = Path(settings.storage_dir) / "speech"
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._whisper_model = None

    def _load_whisper(self):
        if whisper is None:
            raise RuntimeError("Whisper is not installed")
        if self._whisper_model is None:
            self._whisper_model = whisper.load_model(settings.whisper_model)
        return self._whisper_model

    def transcribe(self, audio_path: Path) -> str:
        model = self._load_whisper()
        result = model.transcribe(str(audio_path))
        return result.get("text", "").strip()

    def text_to_speech(self, text: str, output_name: str) -> Path:
        output_path = self.base_dir / f"{output_name}.mp3"
        tts = gTTS(text=text, lang="en")
        tts.save(str(output_path))
        return output_path


speech_service = SpeechService()
