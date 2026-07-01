from pydantic import BaseModel


class CompanyQuestion(BaseModel):
    company: str
    difficulty: str
    topic: str
    question: str


class QuestionBankQuery(BaseModel):
    company: str | None = None
    difficulty: str | None = None
    topic: str | None = None
