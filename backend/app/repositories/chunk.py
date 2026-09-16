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
        
    async def find_by_document_id(
        self,
        document_id: str,
    ) -> list[Chunk]:

        documents = await (
            self.collection
            .find(
                {
                    "document_id": document_id
                }
            )
            .sort("chunk_index", 1)
            .to_list(length=None)
        )

        return [
            Chunk(**document)
            for document in documents
        ]

    async def find_adjacent(
        self,
        document_id: str,
        chunk_index: int,
        radius: int = 2,
    ) -> list[Chunk]:

        if radius < 0:
            raise ValueError(
                "radius must be greater than or equal to zero."
            )

        documents = await (
            self.collection
            .find(
                {
                    "document_id": document_id,
                    "chunk_index": {
                        "$gte": chunk_index - radius,
                        "$lte": chunk_index + radius,
                    },
                }
            )
            .sort("chunk_index", 1)
            .to_list(length=None)
        )

        return [
            Chunk(**document)
            for document in documents
        ]