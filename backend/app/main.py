from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.mongodb import connect_to_mongo, close_mongo
from app.routers import analytics, auth, interview, questions, reports, resumes, voice

app = FastAPI(title="AI Interviewer 5.0", version="5.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event() -> None:
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await close_mongo()


app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(resumes.router, prefix="/api/resumes", tags=["resumes"])
app.include_router(questions.router, prefix="/api/questions", tags=["questions"])
app.include_router(interview.router, prefix="/api/interviews", tags=["interviews"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
app.include_router(voice.router, prefix="/api/voice", tags=["voice"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])


@app.get("/api/health")
async def health() -> dict:
    return {"status": "ok", "service": "ai-interviewer-5.0"}
