from datetime import datetime

from pydantic import BaseModel, Field


class Chunk(BaseModel):
    document_id: str

    chunk_index: int

    text: str

    character_count: int

    embedding: list[float] | None = None

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )