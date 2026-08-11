import fitz

from app.processing.base import BaseProcessor


class PDFProcessor(BaseProcessor):

    async def extract_text(
        self,
        file_path: str,
    ) -> tuple[str, int, list[str]]:

        document = fitz.open(file_path)

        pages = []

        for page in document:
            pages.append(page.get_text())

        page_count = len(document)

        document.close()

        text = "\n".join(pages)

        return text, page_count, pages