from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from app.services.search import SearchService


@pytest.mark.anyio
async def test_search_with_empty_query():
    embedding_model = Mock()
    embedding_service = Mock()
    embedding_service.embedding_model = embedding_model

    vector_repository = AsyncMock()

    service = SearchService(
        embedding_service=embedding_service,
        vector_repository=vector_repository,
    )

    result = await service.search("   ")

    assert result == []

    embedding_model.encode.assert_not_called()
    vector_repository.search.assert_not_awaited()


@pytest.mark.anyio
async def test_search_with_valid_query_generates_embedding():
    embedding_model = Mock()
    embedding_model.encode.return_value = [
        [0.1, 0.2, 0.3]
    ]

    embedding_service = Mock()
    embedding_service.embedding_model = embedding_model

    vector_repository = AsyncMock()
    vector_repository.search.return_value = []

    service = SearchService(
        embedding_service=embedding_service,
        vector_repository=vector_repository,
    )

    result = await service.search(
        query="  machine learning  ",
        limit=5,
    )

    assert result == []

    embedding_model.encode.assert_called_once_with(
        ["machine learning"]
    )

    vector_repository.search.assert_awaited_once_with(
        query_vector=[0.1, 0.2, 0.3],
        limit=5,
        document_id=None,
    )


@pytest.mark.anyio
async def test_search_respects_limit_and_document_id():
    embedding_model = Mock()
    embedding_model.encode.return_value = [
        [0.1, 0.2, 0.3]
    ]

    embedding_service = Mock()
    embedding_service.embedding_model = embedding_model

    vector_repository = AsyncMock()
    vector_repository.search.return_value = []

    service = SearchService(
        embedding_service=embedding_service,
        vector_repository=vector_repository,
    )

    await service.search(
        query="machine learning",
        limit=10,
        document_id="document-123",
    )

    vector_repository.search.assert_awaited_once_with(
        query_vector=[0.1, 0.2, 0.3],
        limit=10,
        document_id="document-123",
    )


@pytest.mark.anyio
async def test_search_maps_qdrant_results_correctly():
    embedding_model = Mock()
    embedding_model.encode.return_value = [
        [0.1, 0.2, 0.3]
    ]

    embedding_service = Mock()
    embedding_service.embedding_model = embedding_model

    vector_repository = AsyncMock()

    vector_repository.search.return_value = [
        SimpleNamespace(
            payload={
                "document_id": "document-1",
                "chunk_index": 2,
                "text": "This is the first matching chunk.",
                "page_number": 4,
            },
            score=0.91,
        ),
        SimpleNamespace(
            payload={
                "document_id": "document-2",
                "chunk_index": 7,
                "text": "This is the second matching chunk.",
                "page_number": 12,
            },
            score=0.83,
        ),
    ]

    service = SearchService(
        embedding_service=embedding_service,
        vector_repository=vector_repository,
    )

    result = await service.search(
        query="machine learning",
        limit=5,
    )

    assert len(result) == 2

    assert result[0].document_id == "document-1"
    assert result[0].chunk_index == 2
    assert result[0].text == "This is the first matching chunk."
    assert result[0].page_number == 4
    assert result[0].score == 0.91

    assert result[1].document_id == "document-2"
    assert result[1].chunk_index == 7
    assert result[1].text == "This is the second matching chunk."
    assert result[1].page_number == 12
    assert result[1].score == 0.83