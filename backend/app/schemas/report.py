from datetime import datetime

from pydantic import BaseModel


class ReportOut(BaseModel):
    id: str
    user_id: str
    interview_id: str
    candidate_name: str
    company: str | None = None
    created_at: datetime
