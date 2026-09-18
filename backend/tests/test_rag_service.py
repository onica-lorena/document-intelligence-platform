from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.schemas.rag import RAGResponse
from app.services.rag import RAGService


@pytest.mark.anyio
async def test_rag_generates_answer_using_search_results():

    search_service = AsyncMock()
    llm = AsyncMock()

    chunk_repository = MagicMock()
    chunk_repository.find_adjacent = AsyncMock(return_value=[])

    search_service.search.return_value = [
        SimpleNamespace(
            document_id="document-1",
            chunk_index=2,
            text="The system supports real-time monitoring.",
            page_number=4,
            score=0.91,
        ),
        SimpleNamespace(
            document_id="document-1",
            chunk_index=5,
            text="The system stores the collected data.",
            page_number=6,
            score=0.84,
        ),
    ]

    llm.generate.return_value = (
        "The system supports real-time monitoring [1] "
        "and stores collected data [2]."
    )

    service = RAGService(
        search_service=search_service,
        llm=llm,
        chunk_repository=chunk_repository,
    )

    result = await service.answer(
        query="What does the system do?",
        limit=5,
    )

    assert isinstance(result, RAGResponse)

    assert result.answer == (
        "The system supports real-time monitoring [1] "
        "and stores collected data [2]."
    )

    assert len(result.sources) == 2

    assert result.sources[0].citation_id == 1
    assert result.sources[0].document_id == "document-1"
    assert result.sources[0].chunk_index == 2
    assert result.sources[0].page_number == 4

    assert result.sources[1].citation_id == 2
    assert result.sources[1].document_id == "document-1"
    assert result.sources[1].chunk_index == 5
    assert result.sources[1].page_number == 6

    search_service.search.assert_awaited_once_with(
        query="What does the system do?",
        limit=5,
        document_id=None,
    )

    chunk_repository.find_adjacent.assert_any_await(
        document_id="document-1",
        chunk_index=2,
        radius=2,
    )

    chunk_repository.find_adjacent.assert_any_await(
        document_id="document-1",
        chunk_index=5,
        radius=2,
    )

    llm.generate.assert_awaited_once()

@pytest.mark.anyio
async def test_rag_source_contains_expanded_context():

    search_service = AsyncMock()
    llm = AsyncMock()

    chunk_repository = MagicMock()

    search_service.search.return_value = [
        SimpleNamespace(
            document_id="document-1",
            chunk_index=4,
            text="Languages: Romanian, English, German.",
            page_number=4,
            score=0.90,
        )
    ]

    chunk_repository.find_adjacent = AsyncMock(
        return_value=[
            SimpleNamespace(
                document_id="document-1",
                chunk_index=3,
                text="Expected Graduation: 2026",
                page_number=3,
            ),
            SimpleNamespace(
                document_id="document-1",
                chunk_index=4,
                text="Languages: Romanian, English, German.",
                page_number=4,
            ),
        ]
    )

    llm.generate.return_value = (
        "Lorena-Andreea Onica is expected to graduate in 2026 [1]."
    )

    service = RAGService(
        search_service=search_service,
        llm=llm,
        chunk_repository=chunk_repository,
    )

    result = await service.answer(
        query="When is Lorena-Andreea Onica expected to graduate?",
        limit=5,
    )

    assert len(result.sources) == 1

    assert result.sources[0].citation_id == 1
    assert result.sources[0].chunk_index == 4

    assert "Expected Graduation: 2026" in result.sources[0].text
    assert "Languages: Romanian, English, German." in result.sources[0].text


@pytest.mark.anyio
async def test_rag_returns_message_when_no_results_are_found():

    search_service = AsyncMock()
    llm = AsyncMock()

    chunk_repository = MagicMock()
    chunk_repository.find_adjacent = AsyncMock(return_value=[])

    search_service.search.return_value = []

    service = RAGService(
        search_service=search_service,
        llm=llm,
        chunk_repository=chunk_repository,
    )

    result = await service.answer(
        query="Something unrelated",
    )

    assert result.answer == (
        "I could not find relevant information "
        "in the provided documents."
    )

    assert result.sources == []

    chunk_repository.find_adjacent.assert_not_awaited()
    llm.generate.assert_not_awaited()


@pytest.mark.anyio
async def test_rag_handles_empty_query():

    search_service = AsyncMock()
    llm = AsyncMock()

    chunk_repository = MagicMock()
    chunk_repository.find_adjacent = AsyncMock(return_value=[])

    service = RAGService(
        search_service=search_service,
        llm=llm,
        chunk_repository=chunk_repository,
    )

    result = await service.answer(
        query="   ",
    )

    assert result.answer == "Please provide a question."

    assert result.sources == []

    search_service.search.assert_not_awaited()
    chunk_repository.find_adjacent.assert_not_awaited()
    llm.generate.assert_not_awaited()