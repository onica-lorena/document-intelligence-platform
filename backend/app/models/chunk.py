from datetime import datetime, timezone

from pydantic import BaseModel, Field


class Chunk(BaseModel):
    document_id: str

    chunk_index: int

    text: str

    character_count: int

    page_number: int | None = None

    embedding: list[float] | None = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )