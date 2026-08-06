from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class DocumentStatus(str, Enum):
    UPLOADED = "UPLOADED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Document(BaseModel):
    filename: str
    stored_filename: str
    storage_path: str
    file_size: int
    content_type: str

    status: DocumentStatus = DocumentStatus.UPLOADED

    text: str | None = None

    page_count: int | None = None

    processing_error: str | None = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)