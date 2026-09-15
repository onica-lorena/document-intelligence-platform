from typing import Any

from app.embeddings.base import BaseEmbeddingModel
from app.models.chunk import Chunk


class EmbeddingService:

    def __init__(
        self,
        embedding_model: BaseEmbeddingModel,
    ):
        self.embedding_model = embedding_model

    @property
    def tokenizer(self) -> Any:
        return self.embedding_model.tokenizer

    @property
    def max_input_length(self) -> int:
        return self.embedding_model.max_input_length

    def embed_query(
        self,
        query: str,
    ) -> list[float]:
        return self.embedding_model.encode([query])[0]

    def embed_chunks(
        self,
        chunks: list[Chunk],
    ) -> list[Chunk]:
        if not chunks:
            return []

        texts = [chunk.text for chunk in chunks]

        embeddings = self.embedding_model.encode(texts)

        for chunk, embedding in zip(chunks, embeddings, strict=True):
            chunk.embedding = embedding

        return chunks