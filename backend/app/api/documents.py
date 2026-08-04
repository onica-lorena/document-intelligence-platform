from fastapi import APIRouter, Depends, File, UploadFile

from app.dependencies.database import get_db
from app.dependencies.storage import get_storage
from app.repositories.document import DocumentRepository
from app.schemas.document import DocumentResponse
from app.services.document import DocumentService
from app.storage.local import LocalStorage

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
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

    service = DocumentService(
        repository=repository,
        storage=storage,
    )

    document_id, document = await service.upload_document(file=file)

    return DocumentResponse(
        id=document_id,
        filename=document.filename,
        content_type=document.content_type,
        created_at=document.created_at,
        status=document.status,
    )