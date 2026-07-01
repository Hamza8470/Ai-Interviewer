from datetime import timedelta, timezone, datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import settings
from app.core.dependencies import get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.db.mongodb import users_collection
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest
from app.schemas.user import UserProfileUpdate
from app.utils.serializers import serialize_doc

router = APIRouter()


@router.post("/register", response_model=AuthResponse)
async def register(payload: RegisterRequest):
    existing = await users_collection().find_one({"email": payload.email.lower()})
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    now = datetime.now(timezone.utc)
    user_id = uuid4().hex
    user = {
        "id": user_id,
        "name": payload.name,
        "email": payload.email.lower(),
        "password_hash": hash_password(payload.password),
        "created_at": now,
        "updated_at": now,
        "target_role": "Software Engineer",
        "experience_level": "Intermediate",
        "company_target": "",
    }
    await users_collection().insert_one(user)
    token = create_access_token(subject=user_id, expires_delta=timedelta(minutes=settings.jwt_access_token_expire_minutes))
    safe_user = serialize_doc(user)
    safe_user.pop("password_hash", None)
    return {"user": safe_user, "access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=AuthResponse)
async def login(payload: LoginRequest):
    user = await users_collection().find_one({"email": payload.email.lower()})
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(subject=user["id"])
    safe_user = serialize_doc(user)
    safe_user.pop("password_hash", None)
    return {"user": safe_user, "access_token": token, "token_type": "bearer"}


@router.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    return serialize_doc(current_user)


@router.patch("/me")
async def update_me(payload: UserProfileUpdate, current_user: dict = Depends(get_current_user)):
    updates = {key: value for key, value in payload.model_dump().items() if value is not None}
    if updates:
        updates["updated_at"] = datetime.now(timezone.utc)
        await users_collection().update_one({"id": current_user["id"]}, {"$set": updates})
    updated_user = await users_collection().find_one({"id": current_user["id"]})
    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    updated_user.pop("password_hash", None)
    return serialize_doc(updated_user)
