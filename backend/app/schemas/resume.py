from datetime import datetime

from pydantic import BaseModel


class ResumeOut(BaseModel):
    id: str
    user_id: str
    filename: str
    text_length: int
    uploaded_at: datetime
