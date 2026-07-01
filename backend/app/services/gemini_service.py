from __future__ import annotations

import json
import re
from typing import Any

from app.core.config import settings

try:
    import google.generativeai as genai
except Exception:  # pragma: no cover - optional dependency fallback
    genai = None


class GeminiService:
    def __init__(self) -> None:
        self.enabled = bool(settings.gemini_api_key) and genai is not None
        if self.enabled:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel(settings.gemini_model)
        else:
            self.model = None

    def _fallback_questions(self, context: str, length: int, company: str | None, role: str | None) -> list[str]:
        topics = ["React", "Node.js", "MongoDB", "System Design", "Problem Solving"]
        prefix = f"{company or 'Target company'} {role or 'interview'}"
        return [f"{prefix}: Explain {topics[i % len(topics)]} concepts from the resume context: {context[:80]}" for i in range(length)]

    def _fallback_evaluation(self, question: str, answer: str) -> dict[str, Any]:
        technical = min(10, max(1, 5 + len(answer.split()) // 25))
        communication = min(10, max(1, 5 + len(answer.splitlines()) // 2))
        return {
            "technical_score": technical,
            "communication_score": communication,
            "strengths": ["Clear intent", "Relevant keywords"],
            "weaknesses": ["Needs deeper examples"],
            "correct_answer": "Provide a structured, example-backed answer.",
            "feedback": f"Your answer to '{question}' shows baseline understanding. Add metrics, examples, and tradeoffs.",
        }

    def _parse_json(self, text: str) -> dict[str, Any]:
        cleaned = text.strip()
        match = re.search(r"\{.*\}", cleaned, re.S)
        if match:
            cleaned = match.group(0)
        return json.loads(cleaned)

    async def generate_questions(self, resume_context: str, length: int, company: str | None, role: str | None, difficulty: str = "medium") -> list[str]:
        if not self.enabled:
            return self._fallback_questions(resume_context, length, company, role)

        prompt = f"""
You are an expert interviewer.
Generate exactly {length} personalized interview questions for a candidate.
Inputs:
- Company: {company or 'Any'}
- Role: {role or 'Software Engineer'}
- Difficulty: {difficulty}
- Resume context: {resume_context}
Return JSON only in this format:
{{"questions": ["q1", "q2"]}}
"""
        response = self.model.generate_content(prompt)
        data = self._parse_json(response.text)
        questions = data.get("questions", [])
        return [str(question) for question in questions][:length] or self._fallback_questions(resume_context, length, company, role)

    async def evaluate_answer(self, question: str, answer: str, resume_context: str, expected_difficulty: str = "medium") -> dict[str, Any]:
        if not self.enabled:
            return self._fallback_evaluation(question, answer)

        prompt = f"""
You are scoring a mock interview response.
Question: {question}
Candidate answer: {answer}
Resume context: {resume_context}
Expected difficulty: {expected_difficulty}
Return JSON only with keys technical_score, communication_score, strengths, weaknesses, correct_answer, feedback.
Scores must be integers from 1 to 10.
"""
        response = self.model.generate_content(prompt)
        data = self._parse_json(response.text)
        return {
            "technical_score": int(data.get("technical_score", 5)),
            "communication_score": int(data.get("communication_score", 5)),
            "strengths": data.get("strengths", []),
            "weaknesses": data.get("weaknesses", []),
            "correct_answer": data.get("correct_answer", ""),
            "feedback": data.get("feedback", ""),
        }

    async def next_question(self, resume_context: str, previous_answers: list[str], current_difficulty: str, topic_hint: str | None = None) -> str:
        if not self.enabled:
            topic = topic_hint or "the main skill area"
            return f"Explain a practical project where you used {topic} and the tradeoffs you made."

        prompt = f"""
Generate one next interview question.
Resume context: {resume_context}
Previous answers: {previous_answers}
Current difficulty: {current_difficulty}
Topic hint: {topic_hint or 'general'}
Return only the question text.
"""
        response = self.model.generate_content(prompt)
        return response.text.strip().strip('"')


gemini_service = GeminiService()
