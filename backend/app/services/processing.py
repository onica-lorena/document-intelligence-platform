from app.models.document import DocumentStatus
from app.processing.pdf_processor import PDFProcessor
from app.repositories.document import DocumentRepository


class ProcessingService:

    def __init__(
        self,
        repository: DocumentRepository,
    ):
        self.repository = repository
        self.pdf_processor = PDFProcessor()

    async def process_document(
        self,
        document_id: str,
    ) -> None:

        document = await self.repository.find_by_id(document_id)

        if document is None:
            raise ValueError("Document not found.")

        try:
            await self.repository.update_status(
                document_id,
                DocumentStatus.PROCESSING,
            )

            text, page_count = await self.pdf_processor.extract_text(
                document.storage_path,
            )

            await self.repository.update_processing_result(
                document_id=document_id,
                text=text,
                page_count=page_count,
            )

        except Exception as exc:
            await self.repository.mark_as_failed(
                document_id,
                str(exc),
            )

            raise