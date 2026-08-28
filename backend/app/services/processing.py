from app.models.document import DocumentStatus
from app.processing.cleaner import TextCleaner
from app.processing.pdf_processor import PDFProcessor
from app.processing.text_splitter import TextSplitter
from app.repositories.chunk import ChunkRepository
from app.repositories.document import DocumentRepository
from app.services.embedding import EmbeddingService
from app.vectorstore.repository import VectorRepository


class ProcessingService:
    def __init__(
        self,
        document_repository: DocumentRepository,
        chunk_repository: ChunkRepository,
        embedding_service: EmbeddingService,
        vector_repository: VectorRepository,
    ):
        self.document_repository = document_repository
        self.chunk_repository = chunk_repository
        self.embedding_service = embedding_service
        self.vector_repository = vector_repository

        self.pdf_processor = PDFProcessor()
        self.text_cleaner = TextCleaner()
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

            text, page_count, pages = (
                await self.pdf_processor.extract_text(
                    document.storage_path,
                )
            )

            cleaned_text = self.text_cleaner.clean(text)
            cleaned_pages = self.text_cleaner.clean_pages(pages)

            chunks = []
            chunk_index = 0

            for page_number, page_text in enumerate(
                cleaned_pages,
                start=1,
            ):
                page_chunks = self.text_splitter.split(
                    document_id=document_id,
                    text=page_text,
                    page_number=page_number,
                    start_index=chunk_index,
                )

                chunks.extend(page_chunks)
                chunk_index += len(page_chunks)

            chunks = self.embedding_service.embed_chunks(
                chunks
            )

            await self.vector_repository.upsert_chunks(
                chunks
            )

            await self.chunk_repository.bulk_create(
                chunks
            )

            await self.document_repository.update_processing_result(
                document_id=document_id,
                text=cleaned_text,
                page_count=page_count,
            )

        except Exception as exc:
            await self.document_repository.mark_as_failed(
                document_id,
                str(exc),
            )
            raise