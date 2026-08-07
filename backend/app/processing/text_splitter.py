from app.models.chunk import Chunk


class TextSplitter:

    def split(
        self,
        *,
        document_id: str,
        text: str,
        chunk_size: int = 1000,
    ) -> list[Chunk]:

        chunks = []

        start = 0
        index = 0

        while start < len(text):

            chunk_text = text[start:start + chunk_size]

            chunks.append(
                Chunk(
                    document_id=document_id,
                    chunk_index=index,
                    text=chunk_text,
                    character_count=len(chunk_text),
                )
            )

            index += 1

            start += chunk_size

        return chunks