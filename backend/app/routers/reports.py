from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from app.core.dependencies import get_current_user
from app.db.mongodb import reports_collection
from app.utils.serializers import serialize_doc

router = APIRouter()


@router.get("")
async def list_reports(current_user: dict = Depends(get_current_user)):
    cursor = reports_collection().find({"user_id": current_user["id"]}).sort("created_at", -1)
    reports = [serialize_doc(doc) async for doc in cursor]
    return {"reports": reports}


@router.get("/{report_id}")
async def get_report(report_id: str, current_user: dict = Depends(get_current_user)):
    report = await reports_collection().find_one({"id": report_id, "user_id": current_user["id"]})
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"report": serialize_doc(report)}


@router.get("/{report_id}/download")
async def download_report(report_id: str, current_user: dict = Depends(get_current_user)):
    report = await reports_collection().find_one({"id": report_id, "user_id": current_user["id"]})
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(report["pdf_path"], media_type="application/pdf", filename="interview-report.pdf")
