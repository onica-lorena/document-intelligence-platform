from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

import app.vectorstore.repository as repository_module
from app.vectorstore.repository import VectorRepository


@pytest.mark.anyio
async def test_vector_search_calls_qdrant_with_correct_parameters(
    monkeypatch,
):
    query_points = AsyncMock(
        return_value=SimpleNamespace(
            points=[]
        )
    )

    monkeypatch.setattr(
        repository_module.qdrant_client,
        "query_points",
        query_points,
    )

    repository = VectorRepository()

    query_vector = [0.1, 0.2, 0.3]

    result = await repository.search(
        query_vector=query_vector,
        limit=5,
    )

    assert result == []

    query_points.assert_awaited_once_with(
        collection_name=repository_module.settings.QDRANT_COLLECTION,
        query=query_vector,
        query_filter=None,
        limit=5,
        with_payload=True,
    )


@pytest.mark.anyio
async def test_vector_search_respects_limit(
    monkeypatch,
):
    query_points = AsyncMock(
        return_value=SimpleNamespace(
            points=[]
        )
    )

    monkeypatch.setattr(
        repository_module.qdrant_client,
        "query_points",
        query_points,
    )

    repository = VectorRepository()

    await repository.search(
        query_vector=[0.1, 0.2, 0.3],
        limit=10,
    )

    query_points.assert_awaited_once()

    call_kwargs = query_points.await_args.kwargs

    assert call_kwargs["limit"] == 10


@pytest.mark.anyio
async def test_vector_search_filters_by_document_id(
    monkeypatch,
):
    query_points = AsyncMock(
        return_value=SimpleNamespace(
            points=[]
        )
    )

    monkeypatch.setattr(
        repository_module.qdrant_client,
        "query_points",
        query_points,
    )

    repository = VectorRepository()

    await repository.search(
        query_vector=[0.1, 0.2, 0.3],
        limit=5,
        document_id="document-123",
    )

    query_points.assert_awaited_once()

    call_kwargs = query_points.await_args.kwargs

    query_filter = call_kwargs["query_filter"]

    assert query_filter is not None
    assert len(query_filter.must) == 1

    condition = query_filter.must[0]

    assert condition.key == "document_id"
    assert condition.match.value == "document-123"


@pytest.mark.anyio
async def test_vector_search_returns_qdrant_points(
    monkeypatch,
):
    points = [
        SimpleNamespace(
            payload={
                "document_id": "document-1",
                "chunk_index": 0,
                "text": "First chunk",
                "page_number": 1,
            },
            score=0.95,
        ),
        SimpleNamespace(
            payload={
                "document_id": "document-1",
                "chunk_index": 1,
                "text": "Second chunk",
                "page_number": 2,
            },
            score=0.88,
        ),
    ]

    query_points = AsyncMock(
        return_value=SimpleNamespace(
            points=points
        )
    )

    monkeypatch.setattr(
        repository_module.qdrant_client,
        "query_points",
        query_points,
    )

    repository = VectorRepository()

    result = await repository.search(
        query_vector=[0.1, 0.2, 0.3],
        limit=5,
    )

    assert result == points

    assert len(result) == 2

    assert result[0].payload["document_id"] == "document-1"
    assert result[0].payload["chunk_index"] == 0
    assert result[0].payload["page_number"] == 1
    assert result[0].score == 0.95

    assert result[1].payload["document_id"] == "document-1"
    assert result[1].payload["chunk_index"] == 1
    assert result[1].payload["page_number"] == 2
    assert result[1].score == 0.88