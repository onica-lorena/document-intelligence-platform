from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    limit: int = Field(default=5, ge=1, le=20)
    document_id: str | None = None


class SearchResult(BaseModel):
    document_id: str
    chunk_index: int
    text: str
    page_number: int | None = None
    score: float