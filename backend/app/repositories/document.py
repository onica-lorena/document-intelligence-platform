from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.document import Document


class DocumentRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["documents"]

    async def create(self, document: Document) -> str:
        result = await self.collection.insert_one(
            document.model_dump()
        )

        return str(result.inserted_id)