from datetime import datetime

from pydantic import BaseModel


class DocumentCreate(BaseModel):
    filename: str
    content_type: str


class DocumentResponse(BaseModel):
    id: str
    filename: str
    content_type: str
    uploaded_at: datetime
    status: str