from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.db.mongodb import close_mongo, connect_to_mongo, questions_collection
from app.seed.company_questions import COMPANY_QUESTIONS, normalize_company_question


async def seed_company_questions() -> None:
    await connect_to_mongo()
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
    print({"inserted": inserted, "updated": updated, "total": len(COMPANY_QUESTIONS)})
    await close_mongo()


if __name__ == "__main__":
    asyncio.run(seed_company_questions())
