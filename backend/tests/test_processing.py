from unittest.mock import AsyncMock

import pytest

from app.models.document import Document, DocumentStatus
from app.services.processing import ProcessingService


@pytest.mark.anyio
async def test_process_document_success():
    document = Document(
        filename="test.pdf",
        stored_filename="test.pdf",
        storage_path="storage/test.pdf",
        file_size=100,
        content_type="application/pdf",
    )

    document_repository = AsyncMock()
    chunk_repository = AsyncMock()

    document_repository.find_by_id.return_value = document

    service = ProcessingService(
        document_repository=document_repository,
        chunk_repository=chunk_repository,
    )

    service.pdf_processor.extract_text = AsyncMock(
        return_value=(
            "Page one text\nPage two text",
            2,
            [
                "Page one text",
                "Page two text",
            ],
        )
    )

    await service.process_document("document-1")

    document_repository.find_by_id.assert_awaited_once_with(
        "document-1"
    )

    document_repository.update_status.assert_awaited_once_with(
        "document-1",
        DocumentStatus.PROCESSING,
    )

    chunk_repository.bulk_create.assert_awaited_once()

    document_repository.update_processing_result.assert_awaited_once_with(
        document_id="document-1",
        text="Page one text\nPage two text",
        page_count=2,
    )

    document_repository.mark_as_failed.assert_not_awaited()

@pytest.mark.anyio
async def test_process_document_failure():
    document = Document(
        filename="test.pdf",
        stored_filename="test.pdf",
        storage_path="storage/test.pdf",
        file_size=100,
        content_type="application/pdf",
    )

    document_repository = AsyncMock()
    chunk_repository = AsyncMock()

    document_repository.find_by_id.return_value = document

    service = ProcessingService(
        document_repository=document_repository,
        chunk_repository=chunk_repository,
    )

    error = RuntimeError("Failed to extract PDF text.")

    service.pdf_processor.extract_text = AsyncMock(
        side_effect=error
    )

    with pytest.raises(RuntimeError, match="Failed to extract PDF text."):
        await service.process_document("document-1")

    document_repository.update_status.assert_awaited_once_with(
        "document-1",
        DocumentStatus.PROCESSING,
    )

    document_repository.mark_as_failed.assert_awaited_once_with(
        "document-1",
        "Failed to extract PDF text.",
    )

    chunk_repository.bulk_create.assert_not_awaited()

    document_repository.update_processing_result.assert_not_awaited()