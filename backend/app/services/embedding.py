from app.embeddings.base import BaseEmbeddingModel
from app.models.chunk import Chunk


class EmbeddingService:

    def __init__(
        self,
        embedding_model: BaseEmbeddingModel,
    ):
        self.embedding_model = embedding_model

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