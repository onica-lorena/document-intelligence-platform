from fastapi import UploadFile
from app.repositories.document import DocumentRepository
from app.models.document import Document
from app.models.storage import StoredFile
from app.models.document import Document, DocumentStatus

class DocumentService:

    def __init__(
        self,
        repository: DocumentRepository,
    ):
        self.repository = repository
        
    async def upload_document(
        self,
        file: UploadFile,
        stored_file: StoredFile,
    ) -> Document:
        document = Document(
            filename=file.filename,
            stored_filename=stored_file.stored_filename,
            storage_path=stored_file.storage_path,
            file_size=stored_file.file_size,
            content_type=file.content_type,
            status=DocumentStatus.UPLOADED,
        )

        await self.repository.create(document)

        return document