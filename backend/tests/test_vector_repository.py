from unittest.mock import AsyncMock, patch
from uuid import uuid5, NAMESPACE_URL
import pytest

from app.models.chunk import Chunk
from app.vectorstore.repository import VectorRepository


@pytest.mark.anyio
async def test_upsert_chunks():
    chunks = [
        Chunk(
            document_id="document-1",
            chunk_index=0,
            text="First chunk",
            character_count=11,
            page_number=1,
            embedding=[0.1, 0.2, 0.3],
        ),
        Chunk(
            document_id="document-1",
            chunk_index=1,
            text="Second chunk",
            character_count=12,
            page_number=1,
            embedding=[0.4, 0.5, 0.6],
        ),
    ]

    repository = VectorRepository()

    with patch(
        "app.vectorstore.repository.qdrant_client.upsert",
        new_callable=AsyncMock,
    ) as mock_upsert:

        await repository.upsert_chunks(chunks)

    mock_upsert.assert_awaited_once()

    call_kwargs = mock_upsert.await_args.kwargs

    assert call_kwargs["collection_name"]

    points = call_kwargs["points"]

    assert len(points) == 2

    expected_id = str(
        uuid5(
            NAMESPACE_URL,
            "document-1:0",
        )
    )

    assert points[0].id == expected_id
    assert points[0].vector == [0.1, 0.2, 0.3]

    assert points[0].payload["document_id"] == "document-1"
    assert points[0].payload["chunk_index"] == 0
    assert points[0].payload["text"] == "First chunk"
    assert points[0].payload["page_number"] == 1

    expected_id = str(
        uuid5(
            NAMESPACE_URL,
            "document-1:1",
        )
    )

    assert points[1].id == expected_id
    assert points[1].vector == [0.4, 0.5, 0.6]

@pytest.mark.anyio
async def test_upsert_chunks_with_empty_list():

    repository = VectorRepository()

    with patch(
        "app.vectorstore.repository.qdrant_client.upsert",
        new_callable=AsyncMock,
    ) as mock_upsert:

        await repository.upsert_chunks([])

    mock_upsert.assert_not_awaited()