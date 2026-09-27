from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from .ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
_generator = None


class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2)
    parties: str = Field(..., min_length=2)
    terms: str = Field(..., min_length=2)
    dates: str = Field(..., min_length=2)


def get_generator() -> GeminiDocumentGenerator:
    global _generator
    if _generator is None:
        _generator = GeminiDocumentGenerator()
    return _generator


@router.get("/health")
def health():
    return {"status": "ok", "service": "LegalEase API"}


@router.post("/generate")
def generate_legal_document(request: DocumentRequest):
    try:
        generator = get_generator()
        document = generator.generate_document(
            request.document_type,
            request.parties,
            request.terms,
            request.dates,
        )
        return {"document": document}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
