from app.schemas.search import SearchResult
from app.services.embedding import EmbeddingService
from app.vectorstore.repository import VectorRepository


class SearchService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_repository: VectorRepository,
    ):
        self.embedding_service = embedding_service
        self.vector_repository = vector_repository

    async def search(
        self,
        query: str,
        limit: int = 5,
        document_id: str | None = None,
    ) -> list[SearchResult]:
        query = query.strip()

        if not query:
            return []

        query_embedding = self.embedding_service.embed_query(query)

        points = await self.vector_repository.search(
            query_vector=query_embedding,
            limit=limit,
            document_id=document_id,
        )

        results = []

        for point in points:
            payload = point.payload or {}

            results.append(
                SearchResult(
                    document_id=payload["document_id"],
                    chunk_index=payload["chunk_index"],
                    text=payload["text"],
                    page_number=payload.get("page_number"),
                    score=point.score,
                )
            )

        return results