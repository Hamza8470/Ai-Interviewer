from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.db.mongodb import interviews_collection, resumes_collection, reports_collection
from app.schemas.interview import AnswerRequest, StartInterviewRequest
from app.services.gemini_service import gemini_service
from app.services.interview_engine import interview_engine
from app.services.report_service import report_service
from app.utils.serializers import serialize_doc

router = APIRouter()


def _get_average(scores: list[float]) -> float:
    return round(sum(scores) / len(scores), 2) if scores else 0.0


@router.post("/start")
async def start_interview(payload: StartInterviewRequest, current_user: dict = Depends(get_current_user)):
    resume = await resumes_collection().find_one({"user_id": current_user["id"]}, sort=[("uploaded_at", -1)])
    if not resume:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Upload a resume before starting an interview")

    session = interview_engine.create_session_payload(current_user["id"], payload.interview_length, payload.company, payload.role)
    resume_context = resume.get("text", "")
    questions = await interview_engine.build_initial_questions(resume_context, payload.interview_length, payload.company, payload.role)
    session["questions"] = [
        {"id": uuid4().hex, "text": question, "difficulty": "medium", "topic": payload.role or "General"}
        for question in questions
    ]
    session["resume_id"] = resume["id"]
    session["resume_context"] = resume_context
    await interviews_collection().insert_one(session)
    return {"interview": serialize_doc(session)}


@router.get("/{interview_id}")
async def get_interview(interview_id: str, current_user: dict = Depends(get_current_user)):
    interview = await interviews_collection().find_one({"id": interview_id, "user_id": current_user["id"]})
    if not interview:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview not found")
    return {"interview": serialize_doc(interview)}


@router.post("/answer")
async def answer_question(payload: AnswerRequest, current_user: dict = Depends(get_current_user)):
    interview = await interviews_collection().find_one({"id": payload.interview_id, "user_id": current_user["id"]})
    if not interview:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview not found")

    questions = interview.get("questions", [])
    question = next((item for item in questions if item["id"] == payload.question_id), None)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

    resume_context = interview.get("resume_context", "")
    evaluation = await gemini_service.evaluate_answer(question["text"], payload.answer, resume_context, question.get("difficulty", "medium"))
    evaluations = interview.get("evaluations", []) + [
        {
            "question_id": payload.question_id,
            "question": question["text"],
            "answer": payload.answer,
            "audio_transcript": payload.audio_transcript,
            "evaluation": evaluation,
            "created_at": datetime.now(timezone.utc),
        }
    ]
    answers = interview.get("answers", []) + [payload.answer]
    technical_scores = [item["evaluation"]["technical_score"] for item in evaluations]
    communication_scores = [item["evaluation"]["communication_score"] for item in evaluations]
    technical_score = _get_average(technical_scores)
    communication_score = _get_average(communication_scores)
    next_difficulty = interview_engine.difficulty_for_score((technical_score + communication_score) / 2)
    next_question = None
    if len(evaluations) < interview.get("length", 5):
        next_question_text = await interview_engine.next_dynamic_question(resume_context, answers, technical_score, question.get("topic"))
        next_question = {"id": uuid4().hex, "text": next_question_text, "difficulty": next_difficulty, "topic": question.get("topic", "General")}
        questions.append(next_question)

    finished = len(evaluations) >= interview.get("length", 5)
    updates = {
        "questions": questions,
        "answers": answers,
        "evaluations": evaluations,
        "technical_score": technical_score,
        "communication_score": communication_score,
        "current_question_index": len(evaluations),
        "updated_at": datetime.now(timezone.utc),
    }
    if finished:
        updates["status"] = "completed"
    await interviews_collection().update_one({"id": interview["id"]}, {"$set": updates})

    response = {
        "evaluation": evaluation,
        "technical_score": technical_score,
        "communication_score": communication_score,
        "next_question": next_question,
        "finished": finished,
    }

    if finished:
        report_payload = {
            "id": uuid4().hex,
            "user_id": current_user["id"],
            "interview_id": interview["id"],
            "candidate_name": current_user.get("name", "Candidate"),
            "company": interview.get("company"),
            "technical_score": technical_score,
            "communication_score": communication_score,
            "strong_areas": evaluation.get("strengths", []),
            "weak_areas": evaluation.get("weaknesses", []),
            "recommendations": ["Practice more scenario-based answers", "Add metrics and concrete examples"],
            "feedback": evaluation.get("feedback", ""),
            "created_at": datetime.now(timezone.utc),
        }
        pdf_path = report_service.generate_pdf(report_payload)
        report_payload["pdf_path"] = str(pdf_path)
        await reports_collection().insert_one(report_payload)
        response["report"] = serialize_doc(report_payload)

    return response


@router.get("/user/history")
async def interview_history(current_user: dict = Depends(get_current_user)):
    cursor = interviews_collection().find({"user_id": current_user["id"]}).sort("created_at", -1)
    items = [serialize_doc(doc) async for doc in cursor]
    return {"interviews": items}
