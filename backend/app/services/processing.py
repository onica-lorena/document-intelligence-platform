from app.models.document import DocumentStatus
from app.processing.pdf_processor import PDFProcessor
from app.processing.text_splitter import TextSplitter
from app.repositories.chunk import ChunkRepository
from app.repositories.document import DocumentRepository


class ProcessingService:

    def __init__(
        self,
        document_repository: DocumentRepository,
        chunk_repository: ChunkRepository,
    ):
        self.document_repository = document_repository
        self.chunk_repository = chunk_repository

        self.pdf_processor = PDFProcessor()
        self.text_splitter = TextSplitter()

    async def process_document(
        self,
        document_id: str,
    ) -> None:

        document = await self.document_repository.find_by_id(
            document_id
        )

        if document is None:
            raise ValueError("Document not found.")

        try:
            await self.document_repository.update_status(
                document_id,
                DocumentStatus.PROCESSING,
            )

            text, page_count = await self.pdf_processor.extract_text(
                document.storage_path,
            )

            chunks = self.text_splitter.split(
                document_id=document_id,
                text=text,
            )

            await self.chunk_repository.bulk_create(
                chunks
            )

            await self.document_repository.update_processing_result(
                document_id=document_id,
                text=text,
                page_count=page_count,
            )

        except Exception as exc:
            await self.document_repository.mark_as_failed(
                document_id,
                str(exc),
            )

            raise