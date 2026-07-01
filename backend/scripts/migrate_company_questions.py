from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.db.mongodb import close_mongo, connect_to_mongo, questions_collection
from app.seed.company_questions import build_question_id


async def migrate_company_questions() -> None:
    await connect_to_mongo()
    cursor = questions_collection().find({})
    migrated = 0
    async for document in cursor:
        company = document.get("company")
        difficulty = document.get("difficulty")
        topic = document.get("topic")
        question = document.get("question")
        if not all([company, difficulty, topic, question]):
            continue
        stable_id = document.get("id") or build_question_id(company, difficulty, topic, question)
        updates = {"id": stable_id, "company": company, "difficulty": difficulty, "topic": topic, "question": question}
        result = await questions_collection().update_one({"_id": document["_id"]}, {"$set": updates})
        if result.modified_count > 0:
            migrated += 1
    print({"migrated": migrated})
    await close_mongo()


if __name__ == "__main__":
    asyncio.run(migrate_company_questions())
