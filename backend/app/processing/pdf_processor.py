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
            page_text = page.get_text("text")

            print("=" * 80)
            print("EXTRACTED TEXT:")
            print(repr(page_text[:500]))

            raw = page.get_text("rawdict")

            print("=" * 80)
            print("RAW DICT:")
            print(raw)

            pages.append(page_text)

        page_count = len(document)

        document.close()

        text = "\n".join(pages)

        return text, page_count, pages