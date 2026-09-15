from pydantic import BaseModel, Field


class RAGRequest(BaseModel):
    query: str = Field(min_length=1)
    limit: int = Field(default=5, ge=1, le=10)
    document_id: str | None = None


class RAGSource(BaseModel):
    citation_id: int
    document_id: str
    chunk_index: int
    text: str
    page_number: int | None = None
    score: float


class RAGResponse(BaseModel):
    answer: str
    sources: list[RAGSource]