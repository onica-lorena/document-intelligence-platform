from app.processing.text_splitter import TextSplitter


class FakeTokenizer:

    def encode(
        self,
        text: str,
        add_special_tokens: bool = False,
    ) -> list[int]:
        return list(range(len(text.split())))

    def decode(
        self,
        token_ids: list[int],
        skip_special_tokens: bool = True,
        clean_up_tokenization_spaces: bool = False,
    ) -> str:
        return " ".join(
            f"word-{token_id}"
            for token_id in token_ids
        )


def create_splitter() -> TextSplitter:
    return TextSplitter(
        tokenizer=FakeTokenizer(),
        max_input_length=20,
        character_chunk_size=100,
        token_overlap=5,
    )


def test_split_creates_chunks():

    splitter = create_splitter()

    text = " ".join(
        f"word-{index}"
        for index in range(40)
    )

    chunks = splitter.split(
        document_id="document-1",
        text=text,
    )

    assert len(chunks) >= 2
    assert chunks[0].chunk_index == 0
    assert chunks[1].chunk_index == 1


def test_split_preserves_token_overlap():

    splitter = create_splitter()

    text = " ".join(
        f"word-{index}"
        for index in range(30)
    )

    chunks = splitter.split(
        document_id="document-1",
        text=text,
    )

    assert len(chunks) >= 2

    first_words = chunks[0].text.split()
    second_words = chunks[1].text.split()

    assert first_words[-5:] == second_words[:5]


def test_split_returns_one_chunk_for_short_text():

    splitter = create_splitter()

    text = "This is a short text."

    chunks = splitter.split(
        document_id="document-1",
        text=text,
    )

    assert len(chunks) == 1
    assert chunks[0].document_id == "document-1"
    assert chunks[0].chunk_index == 0


def test_split_preserves_page_number():

    splitter = create_splitter()

    text = "This is a short text."

    chunks = splitter.split(
        document_id="document-1",
        text=text,
        page_number=3,
    )

    assert len(chunks) == 1
    assert chunks[0].page_number == 3


def test_split_respects_start_index():

    splitter = create_splitter()

    text = "This is a short text."

    chunks = splitter.split(
        document_id="document-1",
        text=text,
        start_index=5,
    )

    assert len(chunks) == 1
    assert chunks[0].chunk_index == 5


def test_split_returns_empty_for_empty_text():

    splitter = create_splitter()

    chunks = splitter.split(
        document_id="document-1",
        text="",
    )

    assert chunks == []

def test_split_separates_sections_by_heading():

    splitter = create_splitter()

    text = """PROJECTS
AI Chatbot for BIM Documentation
Developed a React-based frontend.

EDUCATION
Bachelor's Degree in Computer Science
West University of Timisoara
Expected Graduation: 2026

LANGUAGES
Romanian – Native
English – B2
German – A2
"""

    chunks = splitter.split(
        document_id="document-1",
        text=text,
    )

    assert len(chunks) == 3

    assert chunks[0].text.startswith(
        "PROJECTS"
    )

    assert chunks[1].text.startswith(
        "EDUCATION"
    )

    assert "Expected Graduation: 2026" in chunks[1].text

    assert chunks[2].text.startswith(
        "LANGUAGES"
    )

    assert "Expected Graduation: 2026" not in chunks[2].text