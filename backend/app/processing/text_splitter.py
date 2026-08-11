from app.models.chunk import Chunk


class TextSplitter:

    def split(
        self,
        *,
        document_id: str,
        text: str,
        page_number: int | None = None,
        start_index: int = 0,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> list[Chunk]:

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size."
            )

        chunks = []

        start = 0
        index = start_index

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end]

            chunks.append(
                Chunk(
                    document_id=document_id,
                    chunk_index=index,
                    text=chunk_text,
                    character_count=len(chunk_text),
                    page_number=page_number,
                )
            )

            index += 1

            if end >= len(text):
                break

            start += chunk_size - chunk_overlap

        return chunks