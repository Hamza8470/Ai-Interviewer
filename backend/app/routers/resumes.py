from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from app.core.dependencies import get_current_user
from app.db.mongodb import resumes_collection, interviews_collection
from app.services.rag_service import rag_service
from app.services.resume_service import resume_service
from app.utils.serializers import serialize_doc

router = APIRouter()


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF files are supported")

    file_bytes = await file.read()
    saved_path = resume_service.save_resume(current_user["id"], file.filename, file_bytes)
    text = resume_service.extract_text_from_pdf(saved_path)
    chunks = resume_service.chunk_resume(text)
    resume_id = uuid4().hex
    rag_service.build_index(resume_id, chunks)

    doc = {
        "id": resume_id,
        "user_id": current_user["id"],
        "filename": file.filename,
        "stored_path": str(saved_path),
        "text": text,
        "text_length": len(text),
        "chunks": chunks,
        "uploaded_at": datetime.now(timezone.utc),
        "current": True,
    }
    await resumes_collection().update_many({"user_id": current_user["id"]}, {"$set": {"current": False}})
    await resumes_collection().insert_one(doc)
    return {"resume": serialize_doc(doc), "message": "Resume uploaded and indexed successfully"}


@router.get("/latest")
async def get_latest_resume(current_user: dict = Depends(get_current_user)):
    resume = await resumes_collection().find_one({"user_id": current_user["id"]}, sort=[("uploaded_at", -1)])
    if not resume:
        return {"resume": None}
    return {"resume": serialize_doc(resume)}


@router.post("/retrieve")
async def retrieve_resume_context(query: str = Form(...), current_user: dict = Depends(get_current_user)):
    resume = await resumes_collection().find_one({"user_id": current_user["id"]}, sort=[("uploaded_at", -1)])
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Upload a resume first")
    results = rag_service.retrieve(resume["id"], query)
    return {"query": query, "results": results}
