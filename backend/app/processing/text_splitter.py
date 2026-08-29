import re
from typing import Any

from app.models.chunk import Chunk


class TextSplitter:

    def __init__(
        self,
        tokenizer: Any,
        max_input_length: int,
        character_chunk_size: int = 1000,
        token_overlap: int = 50,
    ):
        if token_overlap >= max_input_length:
            raise ValueError(
                "token_overlap must be smaller than max_input_length."
            )

        if character_chunk_size <= 0:
            raise ValueError(
                "character_chunk_size must be greater than zero."
            )

        self.tokenizer = tokenizer
        self.max_input_length = max_input_length
        self.character_chunk_size = character_chunk_size
        self.token_overlap = token_overlap

        # Reserve space for special tokens such as [CLS] and [SEP].
        self.max_content_tokens = max_input_length - 2

    def split(
        self,
        *,
        document_id: str,
        text: str,
        page_number: int | None = None,
        start_index: int = 0,
    ) -> list[Chunk]:

        if not text.strip():
            return []

        sections = self._split_by_structure(text)

        chunks: list[Chunk] = []
        chunk_index = start_index

        for section in sections:
            token_chunks = self._split_by_tokens(section)

            for chunk_text in token_chunks:
                chunks.append(
                    Chunk(
                        document_id=document_id,
                        chunk_index=chunk_index,
                        text=chunk_text,
                        character_count=len(chunk_text),
                        page_number=page_number,
                    )
                )

                chunk_index += 1

        return chunks

    def _split_by_structure(
        self,
        text: str,
    ) -> list[str]:

        paragraphs = [
            paragraph.strip()
            for paragraph in re.split(r"\n\s*\n", text)
            if paragraph.strip()
        ]

        sections: list[str] = []

        for paragraph in paragraphs:

            if len(paragraph) <= self.character_chunk_size:
                sections.append(paragraph)
                continue

            sentences = re.split(
                r"(?<=[.!?])\s+",
                paragraph,
            )

            current_section = ""

            for sentence in sentences:
                sentence = sentence.strip()

                if not sentence:
                    continue

                if not current_section:
                    current_section = sentence
                    continue

                candidate = f"{current_section} {sentence}"

                if len(candidate) <= self.character_chunk_size:
                    current_section = candidate
                else:
                    sections.append(current_section)
                    current_section = sentence

            if current_section:
                sections.append(current_section)

        return sections

    def _split_by_tokens(
        self,
        text: str,
    ) -> list[str]:

        token_ids = self.tokenizer.encode(
            text,
            add_special_tokens=False,
        )

        if len(token_ids) <= self.max_content_tokens:
            return [text]

        chunks: list[str] = []

        step = self.max_content_tokens - self.token_overlap
        start = 0

        while start < len(token_ids):

            end = start + self.max_content_tokens

            chunk_token_ids = token_ids[start:end]

            chunk_text = self.tokenizer.decode(
                chunk_token_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False,
            ).strip()

            if chunk_text:
                chunks.append(chunk_text)

            if end >= len(token_ids):
                break

            start += step

        return chunks