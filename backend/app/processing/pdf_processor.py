from app.processing.base import BaseProcessor


class PDFProcessor(BaseProcessor):

    async def extract_text(self, file_path: str) -> str:
        raise NotImplementedError