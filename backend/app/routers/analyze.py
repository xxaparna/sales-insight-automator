import os
import magic
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import EmailStr

from ..services.parser_service import parse_sales_file
from ..services.ai_service import generate_summary
from ..services.email_service import send_summary_email
from ..models.schemas import AnalyzeResponse

router = APIRouter(prefix="/api/v1", tags=["Analysis"])

ALLOWED_TYPES = {
    "text/csv",
    "application/csv",
    "text/plain",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}

MAX_FILE_SIZE = 5 * 1024 * 1024


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_file(
    file: UploadFile = File(...),
    email: EmailStr = Form(...)
):

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    real_type = magic.from_buffer(contents, mime=True)

    if real_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Invalid file type")

    filename = file.filename or "upload"

    try:
        stats = parse_sales_file(contents, filename)

        summary = generate_summary(stats)

        send_summary_email(email, summary, filename)

        return AnalyzeResponse(
            status="success",
            message=f"Summary sent to {email}",
            summary_preview=summary[:200]
        )

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))