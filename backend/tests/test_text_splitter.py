import pytest

from app.processing.text_splitter import TextSplitter


def test_split_creates_chunks():
    splitter = TextSplitter()

    text = "a" * 2500

    chunks = splitter.split(
        document_id="document-1",
        text=text,
        chunk_size=1000,
        chunk_overlap=200,
    )

    assert len(chunks) == 3


def test_split_preserves_overlap():
    splitter = TextSplitter()

    text = "a" * 1800

    chunks = splitter.split(
        document_id="document-1",
        text=text,
        chunk_size=1000,
        chunk_overlap=200,
    )

    assert len(chunks) == 2
    assert chunks[0].text[-200:] == chunks[1].text[:200]


def test_split_rejects_invalid_overlap():
    splitter = TextSplitter()

    with pytest.raises(ValueError):
        splitter.split(
            document_id="document-1",
            text="some text",
            chunk_size=1000,
            chunk_overlap=1000,
        )

def test_split_returns_one_chunk_for_short_text():
    splitter = TextSplitter()

    text = "This is a short text."

    chunks = splitter.split(
        document_id="document-1",
        text=text,
        chunk_size=1000,
        chunk_overlap=200,
    )

    assert len(chunks) == 1
    assert chunks[0].text == text
    assert chunks[0].chunk_index == 0
    assert chunks[0].character_count == len(text)

def test_split_sets_chunk_metadata():
    splitter = TextSplitter()

    text = "a" * 1500

    chunks = splitter.split(
        document_id="document-123",
        text=text,
        page_number=3,
        start_index=5,
        chunk_size=1000,
        chunk_overlap=200,
    )

    assert chunks[0].document_id == "document-123"
    assert chunks[0].chunk_index == 5
    assert chunks[0].page_number == 3
    assert chunks[0].character_count == 1000