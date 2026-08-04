from fastapi import UploadFile

from app.models.document import Document, DocumentStatus
from app.repositories.document import DocumentRepository
from app.storage.local import LocalStorage


class DocumentService:

    def __init__(
        self,
        repository: DocumentRepository,
        storage: LocalStorage,
    ):
        self.repository = repository
        self.storage = storage

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

        return document_id, document