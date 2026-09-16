from unittest.mock import AsyncMock, MagicMock, Mock

import pytest

from app.repositories.chunk import ChunkRepository


@pytest.mark.anyio
async def test_find_adjacent_returns_chunks_within_radius():

    db = MagicMock()
    collection = MagicMock()

    db.__getitem__.return_value = collection

    documents = [
        {
            "document_id": "document-1",
            "chunk_index": 6,
            "text": "Chunk six",
            "character_count": 9,
            "page_number": 1,
        },
        {
            "document_id": "document-1",
            "chunk_index": 7,
            "text": "Chunk seven",
            "character_count": 11,
            "page_number": 1,
        },
        {
            "document_id": "document-1",
            "chunk_index": 8,
            "text": "Chunk eight",
            "character_count": 11,
            "page_number": 1,
        },
        {
            "document_id": "document-1",
            "chunk_index": 9,
            "text": "Chunk nine",
            "character_count": 10,
            "page_number": 1,
        },
        {
            "document_id": "document-1",
            "chunk_index": 10,
            "text": "Chunk ten",
            "character_count": 10,
            "page_number": 1,
        },
    ]

    cursor = MagicMock()
    sorted_cursor = MagicMock()

    collection.find.return_value = cursor
    cursor.sort.return_value = sorted_cursor

    sorted_cursor.to_list = AsyncMock(
        return_value=documents
    )

    repository = ChunkRepository(db)

    result = await repository.find_adjacent(
        document_id="document-1",
        chunk_index=8,
        radius=2,
    )

    collection.find.assert_called_once_with(
        {
            "document_id": "document-1",
            "chunk_index": {
                "$gte": 6,
                "$lte": 10,
            },
        }
    )

    cursor.sort.assert_called_once_with(
        "chunk_index",
        1,
    )

    sorted_cursor.to_list.assert_awaited_once_with(
        length=None
    )

    assert [chunk.chunk_index for chunk in result] == [
        6,
        7,
        8,
        9,
        10,
    ]

    assert all(
        chunk.document_id == "document-1"
        for chunk in result
    )


@pytest.mark.anyio
async def test_find_adjacent_rejects_negative_radius():

    db = MagicMock()
    collection = Mock()

    db["chunks"] = collection

    repository = ChunkRepository(db)

    with pytest.raises(
        ValueError,
        match="radius must be greater than or equal to zero",
    ):
        await repository.find_adjacent(
            document_id="document-1",
            chunk_index=8,
            radius=-1,
        )