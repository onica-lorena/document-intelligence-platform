from unittest.mock import Mock
import pytest
from app.models.chunk import Chunk
from app.services.embedding import EmbeddingService


def test_embed_chunks():
    embedding_model = Mock()

    embedding_model.encode.return_value = [
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
    ]

    service = EmbeddingService(
        embedding_model=embedding_model,
    )

    chunks = [
        Chunk(
            document_id="document-1",
            chunk_index=0,
            text="First chunk",
            character_count=11,
        ),
        Chunk(
            document_id="document-1",
            chunk_index=1,
            text="Second chunk",
            character_count=12,
        ),
    ]

    result = service.embed_chunks(chunks)

    embedding_model.encode.assert_called_once_with(
        [
            "First chunk",
            "Second chunk",
        ]
    )

    assert result[0].embedding == [0.1, 0.2, 0.3]
    assert result[1].embedding == [0.4, 0.5, 0.6]

def test_embed_chunks_with_empty_list():
    embedding_model = Mock()

    service = EmbeddingService(
        embedding_model=embedding_model,
    )

    result = service.embed_chunks([])

    assert result == []

    embedding_model.encode.assert_not_called()

def test_embed_chunks_raises_when_embedding_count_does_not_match_chunks():
    embedding_model = Mock()

    embedding_model.encode.return_value = [
        [0.1, 0.2, 0.3],
    ]

    service = EmbeddingService(
        embedding_model=embedding_model,
    )

    chunks = [
        Chunk(
            document_id="document-1",
            chunk_index=0,
            text="First chunk",
            character_count=11,
        ),
        Chunk(
            document_id="document-1",
            chunk_index=1,
            text="Second chunk",
            character_count=12,
        ),
    ]

    with pytest.raises(ValueError):
        service.embed_chunks(chunks)

def test_embed_query():
    embedding_model = Mock()

    embedding_model.encode.return_value = [
        [0.1, 0.2, 0.3]
    ]

    service = EmbeddingService(
        embedding_model=embedding_model,
    )

    query = "What is this document about?"

    embedding = service.embed_query(query)

    embedding_model.encode.assert_called_once_with(
        [query]
    )

    assert embedding == [0.1, 0.2, 0.3]