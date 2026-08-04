from datetime import datetime

from pydantic import BaseModel

from app.models.document import DocumentStatus


class DocumentResponse(BaseModel):
    id: str
    filename: str
    content_type: str
    created_at: datetime
    status: DocumentStatus