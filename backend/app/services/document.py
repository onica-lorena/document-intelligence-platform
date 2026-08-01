from app.repositories.document_repository import DocumentRepository
from app.models.document import Document


class DocumentService:
    def __init__(self, repository: DocumentRepository):
        self.repository = repository

    async def create_document(self, document: Document) -> str:
        return await self.repository.create(document)