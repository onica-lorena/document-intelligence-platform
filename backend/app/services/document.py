from fastapi import UploadFile

from app.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddingModel,
)
from app.models.document import Document, DocumentStatus
from app.repositories.chunk import ChunkRepository
from app.repositories.document import DocumentRepository
from app.services.embedding import EmbeddingService
from app.services.processing import ProcessingService
from app.storage.local import LocalStorage


class DocumentService:

    def __init__(
        self,
        repository: DocumentRepository,
        storage: LocalStorage,
    ):
        self.repository = repository
        self.storage = storage

        chunk_repository = ChunkRepository(
            repository.collection.database
        )

        embedding_model = SentenceTransformerEmbeddingModel()

        embedding_service = EmbeddingService(
            embedding_model=embedding_model,
        )

        self.processing_service = ProcessingService(
            document_repository=repository,
            chunk_repository=chunk_repository,
            embedding_service=embedding_service,
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

        document_id = await self.repository.create(
            document
        )

        await self.processing_service.process_document(
            document_id
        )

        document = await self.repository.find_by_id(
            document_id
        )

        return document_id, document