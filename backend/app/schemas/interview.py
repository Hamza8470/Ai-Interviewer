from datetime import datetime
from pydantic import BaseModel, Field


class StartInterviewRequest(BaseModel):
    interview_length: int = Field(default=5, ge=5, le=10)
    company: str | None = None
    role: str | None = None


class AnswerRequest(BaseModel):
    interview_id: str
    question_id: str
    answer: str = Field(min_length=1)
    audio_transcript: str | None = None


class AdaptiveState(BaseModel):
    current_question: str | None = None
    previous_answers: list[str] = []
    technical_score: float = 0.0
    communication_score: float = 0.0
    difficulty: str = "easy"


class InterviewOut(BaseModel):
    id: str
    user_id: str
    status: str
    created_at: datetime
