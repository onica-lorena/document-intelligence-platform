from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi import UploadFile, File

from app.dependencies.storage import get_storage
from app.storage.local import LocalStorage
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

@router.post(
    "/upload",
    response_model=DocumentResponse,
)
async def upload_document(
    file: UploadFile = File(...),
    db=Depends(get_db),
    storage: LocalStorage = Depends(get_storage),
):
    repository = DocumentRepository(db)

    service = DocumentService(repository)

    stored_file = await storage.save(file)

    document = await service.upload_document(
        file=file,
        stored_file=stored_file,
    )

    document_id = await repository.create(document)

    return DocumentResponse(
        id=document_id,
        filename=document.filename,
        content_type=document.content_type,
        created_at=document.created_at,
        status=document.status,
    )

