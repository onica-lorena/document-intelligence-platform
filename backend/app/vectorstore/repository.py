from qdrant_client.models import Distance, PointStruct, VectorParams
from uuid import uuid5, NAMESPACE_URL
from app.core.config import settings
from app.models.chunk import Chunk
from app.vectorstore.client import qdrant_client


class VectorRepository:

    async def create_collection(
        self,
        vector_size: int = 384,
    ) -> None:

        collections = await qdrant_client.get_collections()

        collection_exists = any(
            collection.name == settings.QDRANT_COLLECTION
            for collection in collections.collections
        )

        if collection_exists:
            return

        await qdrant_client.create_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )

    async def upsert_chunks(
        self,
        chunks: list[Chunk],
    ) -> None:

        if not chunks:
            return

        points = [
            PointStruct(
                id=str(
                    uuid5(
                        NAMESPACE_URL,
                        f"{chunk.document_id}:{chunk.chunk_index}",
                    )
                ),
                vector=chunk.embedding,
                payload={
                    "document_id": chunk.document_id,
                    "chunk_index": chunk.chunk_index,
                    "text": chunk.text,
                    "page_number": chunk.page_number,
                },
            )
            for chunk in chunks
        ]

        await qdrant_client.upsert(
            collection_name=settings.QDRANT_COLLECTION,
            points=points,
        )