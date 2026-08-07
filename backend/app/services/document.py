from fastapi import UploadFile

from app.models.document import Document, DocumentStatus
from app.repositories.document import DocumentRepository
from app.storage.local import LocalStorage
from app.services.processing import ProcessingService


class DocumentService:

    def __init__(
        self,
        repository: DocumentRepository,
        storage: LocalStorage,
    ):
        self.repository = repository
        self.storage = storage
        self.processing_service = ProcessingService(
            repository
        )

    async def upload_document(
        self,
        file: UploadFile,
    ) -> tuple[str, Document]:

        stored_file = await self.storage.save(file)

        document = Document(
            filename=file.filename,
            stored_filename=stored_file.stored_filename,
            storage_path=stored_file.storage_path,
            file_size=stored_file.file_size,
            content_type=file.content_type,
            status=DocumentStatus.UPLOADED,
        )

        document_id = await self.repository.create(document)

        await self.processing_service.process_document(
            document_id
        )

        document = await self.repository.find_by_id(
            document_id
        )

        return document_id, document