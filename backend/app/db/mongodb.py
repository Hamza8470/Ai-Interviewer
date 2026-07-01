from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings

client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None


async def connect_to_mongo() -> None:
    global client, _db
    if client is None:
        client = AsyncIOMotorClient(settings.mongodb_uri)
        _db = client[settings.mongodb_db]


async def close_mongo() -> None:
    global client, _db
    if client is not None:
        client.close()
        client = None
        _db = None


def get_db() -> AsyncIOMotorDatabase:
    if _db is None:
        raise RuntimeError("MongoDB connection is not initialized")
    return _db


def users_collection():
    return get_db()["users"]


def interviews_collection():
    return get_db()["interviews"]


def reports_collection():
    return get_db()["reports"]


def questions_collection():
    return get_db()["questions"]


def resumes_collection():
    return get_db()["resumes"]
