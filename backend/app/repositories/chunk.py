from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.chunk import Chunk


class ChunkRepository:

    def __init__(
        self,
        db: AsyncIOMotorDatabase,
    ):
        self.collection = db["chunks"]

    async def bulk_create(
        self,
        chunks: list[Chunk],
    ) -> None:

        if not chunks:
            return

        documents = [
            chunk.model_dump()
            for chunk in chunks
        ]

        await self.collection.insert_many(
            documents
        )