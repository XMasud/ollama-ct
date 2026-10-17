from fastapi import FastAPI

from app.api.v1 import chat
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    docs_url="/docs",
)

app.include_router(
    chat.router, prefix="/api/v1", tags=["Chat"]
)


@app.get("/health")
async def health_check():
    return {"status": "ok", "model": settings.OLLAMA_MODEL}
