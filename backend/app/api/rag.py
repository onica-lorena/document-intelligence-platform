from functools import lru_cache

from fastapi import APIRouter, Depends

from app.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddingModel,
)
from app.llm.ollama import OllamaLLM
from app.schemas.rag import RAGRequest, RAGResponse
from app.services.embedding import EmbeddingService
from app.services.rag import RAGService
from app.services.search import SearchService
from app.vectorstore.repository import VectorRepository
from app.dependencies.database import get_db
from app.repositories.chunk import ChunkRepository


router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)

@lru_cache
def get_rag_service() -> RAGService:
    embedding_model = SentenceTransformerEmbeddingModel()

    embedding_service = EmbeddingService(
        embedding_model=embedding_model,
    )

    vector_repository = VectorRepository()

    search_service = SearchService(
        embedding_service=embedding_service,
        vector_repository=vector_repository,
    )

    llm = OllamaLLM()

    chunk_repository = ChunkRepository(
        get_db()
    )

    return RAGService(
        search_service=search_service,
        llm=llm,
        chunk_repository=chunk_repository,
    )

@router.post(
    "",
    response_model=RAGResponse,
)
async def answer_question(
    request: RAGRequest,
    service: RAGService = Depends(get_rag_service),
):
    return await service.answer(
        query=request.query,
        limit=request.limit,
        document_id=request.document_id,
    )