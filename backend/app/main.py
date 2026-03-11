from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path

from .routers.analyze import router

# Ensure .env is loaded from project root
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(env_path)

app = FastAPI(
    title="Sales Insight Automator API",
    description="Upload sales data and receive AI generated summary via email",
    version="1.0.0"
)

# Allow frontend (Next.js) to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Sales Insight Automator API running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}