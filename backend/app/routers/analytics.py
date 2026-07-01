from __future__ import annotations

from statistics import mean

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.db.mongodb import interviews_collection, reports_collection

router = APIRouter()


@router.get("/dashboard")
async def dashboard(current_user: dict = Depends(get_current_user)):
    interviews = [doc async for doc in interviews_collection().find({"user_id": current_user["id"]})]
    reports = [doc async for doc in reports_collection().find({"user_id": current_user["id"]}).sort("created_at", -1).limit(5)]
    total_interviews = len(interviews)
    avg_score = round(mean([(item.get("technical_score", 0) + item.get("communication_score", 0)) / 2 for item in interviews]), 2) if interviews else 0
    strong_areas = []
    weak_areas = []
    topic_scores: dict[str, list[float]] = {}
    trend = []

    for interview in interviews:
        for evaluation in interview.get("evaluations", []):
            eval_data = evaluation.get("evaluation", {})
            strong_areas.extend(eval_data.get("strengths", []))
            weak_areas.extend(eval_data.get("weaknesses", []))
            topic = evaluation.get("question", "General").split()[0][:20]
            topic_scores.setdefault(topic, []).append((eval_data.get("technical_score", 0) + eval_data.get("communication_score", 0)) / 2)
        trend.append({"label": interview.get("created_at").isoformat() if interview.get("created_at") else "", "score": (interview.get("technical_score", 0) + interview.get("communication_score", 0)) / 2})

    topic_summary = [
        {"topic": topic, "score": round(mean(scores), 2)}
        for topic, scores in topic_scores.items()
    ]

    return {
        "total_interviews": total_interviews,
        "average_score": avg_score,
        "strong_areas": list(dict.fromkeys(strong_areas))[:5],
        "weak_areas": list(dict.fromkeys(weak_areas))[:5],
        "recent_reports": reports,
        "topic_summary": topic_summary,
        "improvement_trend": trend[-10:],
    }
