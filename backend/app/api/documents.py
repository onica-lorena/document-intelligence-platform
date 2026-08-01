from datetime import datetime

from fastapi import APIRouter, Depends

from app.dependencies.database import get_db
from app.models.document import Document, DocumentStatus
from app.repositories.document import DocumentRepository
from app.schemas.document import (
    DocumentCreate,
    DocumentResponse,
)
from app.services.document import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post("", response_model=DocumentResponse)
async def create_document(
    payload: DocumentCreate,
    db=Depends(get_db),
):
    repository = DocumentRepository(db)

    service = DocumentService(repository)

    document = Document(
        filename=payload.filename,
        content_type=payload.content_type,
        status=DocumentStatus.UPLOADED,
    )

    document_id = await service.create_document(document)

    return DocumentResponse(
        id=document_id,
        filename=document.filename,
        content_type=document.content_type,
        created_at=document.created_at,
        status=document.status,
    )