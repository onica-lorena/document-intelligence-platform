from datetime import datetime

from pydantic import BaseModel
from app.models.document import DocumentStatus


class DocumentCreate(BaseModel):
    filename: str
    content_type: str


class DocumentResponse(BaseModel):
    id: str
    filename: str
    content_type: str
    created_at: datetime
    status: DocumentStatus