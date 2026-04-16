from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from app.db.session import engine
from app.db.base import Base
import app.models.api_key  # Register models

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="API Key Management Service",
    description="Backend service for managing API keys and rate limiting.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
