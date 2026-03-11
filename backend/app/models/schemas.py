from pydantic import BaseModel
from typing import Optional


class AnalyzeResponse(BaseModel):
    status: str
    message: str
    summary_preview: Optional[str] = None


class ErrorResponse(BaseModel):
    detail: str