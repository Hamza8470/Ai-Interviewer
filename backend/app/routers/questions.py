from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_current_user
from app.db.mongodb import questions_collection
from app.seed.company_questions import COMPANY_QUESTIONS, normalize_company_question
from app.utils.serializers import serialize_doc

router = APIRouter()


@router.post("/seed")
async def seed_questions(current_user: dict = Depends(get_current_user)):
    inserted = 0
    updated = 0
    for question in COMPANY_QUESTIONS:
        normalized = normalize_company_question(question)
        result = await questions_collection().update_one(
            {"id": normalized["id"]},
            {"$set": normalized},
            upsert=True,
        )
        if result.upserted_id is not None:
            inserted += 1
        elif result.modified_count > 0:
            updated += 1
    return {"inserted": inserted, "updated": updated, "total": len(COMPANY_QUESTIONS)}


@router.get("/bank")
async def get_company_questions(
    company: str | None = Query(default=None),
    difficulty: str | None = Query(default=None),
    topic: str | None = Query(default=None),
    current_user: dict = Depends(get_current_user),
):
    query: dict = {}
    if company:
        query["company"] = company
    if difficulty:
        query["difficulty"] = difficulty
    if topic:
        query["topic"] = topic
    cursor = questions_collection().find(query)
    items = [serialize_doc(doc) async for doc in cursor]
    if not items:
        items = [item for item in COMPANY_QUESTIONS if (not company or item["company"] == company) and (not difficulty or item["difficulty"] == difficulty) and (not topic or item["topic"] == topic)]
    return {"questions": items}
