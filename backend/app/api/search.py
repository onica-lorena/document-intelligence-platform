from functools import lru_cache

from fastapi import APIRouter, Depends

from app.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddingModel,
)
from app.schemas.search import SearchRequest, SearchResult
from app.services.embedding import EmbeddingService
from app.services.search import SearchService
from app.vectorstore.repository import VectorRepository


router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@lru_cache
def get_search_service() -> SearchService:
    embedding_model = SentenceTransformerEmbeddingModel()
    embedding_service = EmbeddingService(
        embedding_model=embedding_model,
    )
    vector_repository = VectorRepository()

    return SearchService(
        embedding_service=embedding_service,
        vector_repository=vector_repository,
    )


@router.post(
    "",
    response_model=list[SearchResult],
)
async def search_documents(
    request: SearchRequest,
    service: SearchService = Depends(get_search_service),
):
    return await service.search(
        query=request.query,
        limit=request.limit,
        document_id=request.document_id,
    )