import fitz

from app.processing.base import BaseProcessor


class PDFProcessor(BaseProcessor):

    async def extract_text(
        self,
        file_path: str,
    ) -> tuple[str, int]:

        document = fitz.open(file_path)

        text = ""

        for page in document:
            text += page.get_text()

        page_count = len(document)

        document.close()

        return text, page_count