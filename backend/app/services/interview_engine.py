from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.seed.company_questions import COMPANY_QUESTIONS
from app.services.gemini_service import gemini_service


class InterviewEngine:
    def difficulty_for_score(self, score: float) -> str:
        if score >= 8:
            return "hard"
        if score >= 5:
            return "medium"
        return "easy"

    async def build_initial_questions(self, resume_context: str, length: int, company: str | None, role: str | None) -> list[str]:
        return await gemini_service.generate_questions(resume_context, length, company, role)

    def select_bank_question(self, company: str | None = None, difficulty: str | None = None, topic: str | None = None) -> dict | None:
        candidates = COMPANY_QUESTIONS
        if company:
            candidates = [item for item in candidates if item["company"].lower() == company.lower()]
        if difficulty:
            candidates = [item for item in candidates if item["difficulty"].lower() == difficulty.lower()]
        if topic:
            candidates = [item for item in candidates if item["topic"].lower() == topic.lower()]
        return candidates[0] if candidates else None

    async def next_dynamic_question(self, resume_context: str, answers: list[str], technical_score: float, topic_hint: str | None = None) -> str:
        difficulty = self.difficulty_for_score(technical_score)
        return await gemini_service.next_question(resume_context, answers, difficulty, topic_hint)

    def create_session_payload(self, user_id: str, length: int, company: str | None, role: str | None) -> dict:
        now = datetime.now(timezone.utc)
        return {
            "id": uuid4().hex,
            "user_id": user_id,
            "status": "active",
            "length": length,
            "company": company,
            "role": role,
            "current_question_index": 0,
            "questions": [],
            "answers": [],
            "evaluations": [],
            "technical_score": 0.0,
            "communication_score": 0.0,
            "created_at": now,
            "updated_at": now,
        }


interview_engine = InterviewEngine()
