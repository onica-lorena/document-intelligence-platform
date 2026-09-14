from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    UploadFile,
    HTTPException,
)

from app.dependencies.database import get_db
from app.dependencies.storage import get_storage
from app.repositories.document import DocumentRepository
from app.schemas.document import DocumentResponse
from app.services.document import DocumentService
from app.storage.local import LocalStorage
from app.repositories.chunk import ChunkRepository

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/upload",
    response_model=DocumentResponse,
)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db=Depends(get_db),
    storage: LocalStorage = Depends(get_storage),
):
    repository = DocumentRepository(db)

    service = DocumentService(
        repository=repository,
        storage=storage,
    )

    document_id, document = await service.upload_document(
        file=file,
    )

    background_tasks.add_task(
        service.process_document,
        document_id,
    )

    return DocumentResponse(
        id=document_id,
        filename=document.filename,
        content_type=document.content_type,
        created_at=document.created_at,
        status=document.status,
    )

@router.get(
    "/{document_id}/chunks",
)
async def get_document_chunks(
    document_id: str,
    db=Depends(get_db),
):
    repository = ChunkRepository(db)

    chunks = await repository.find_by_document_id(
        document_id
    )

    return chunks

@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
async def get_document(
    document_id: str,
    db=Depends(get_db),
):
    repository = DocumentRepository(db)

    document = await repository.find_by_id(
        document_id
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    return DocumentResponse(
        id=document_id,
        filename=document.filename,
        content_type=document.content_type,
        created_at=document.created_at,
        status=document.status,
    )

