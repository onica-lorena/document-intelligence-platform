from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.models.document import Document
from datetime import datetime
from app.models.document import (
    Document,
    DocumentStatus,
)


class DocumentRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["documents"]

    async def create(self, document: Document) -> str:
        result = await self.collection.insert_one(
            document.model_dump()
        )

        return str(result.inserted_id)
    
    async def find_by_id(
        self,
        document_id: str,
    ) -> Document | None:

        document = await self.collection.find_one(
            {
                "_id": ObjectId(document_id)
            }
        )

        if document is None:
            return None

        document.pop("_id")

        return Document(**document)

    async def update_status(
        self,
        document_id: str,
        status: DocumentStatus,
    ) -> None:

        await self.collection.update_one(
            {
                "_id": ObjectId(document_id)
            },
            {
                "$set": {
                    "status": status,
                    "updated_at": datetime.utcnow(),
                }
            },
        )

    async def update_processing_result(
        self,
        document_id: str,
        text: str,
        page_count: int,
    ) -> None:

        await self.collection.update_one(
            {
                "_id": ObjectId(document_id)
            },
            {
                "$set": {
                    "text": text,
                    "page_count": page_count,
                    "status": DocumentStatus.COMPLETED,
                    "processing_error": None,
                    "updated_at": datetime.utcnow(),
                }
            },
        )

    async def mark_as_failed(
        self,
        document_id: str,
        error: str,
    ) -> None:

        await self.collection.update_one(
            {
                "_id": ObjectId(document_id)
            },
            {
                "$set": {
                    "status": DocumentStatus.FAILED,
                    "processing_error": error,
                    "updated_at": datetime.utcnow(),
                }
            },
        )