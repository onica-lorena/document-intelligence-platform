import fitz
from PIL import Image

from app.processing.base import BaseProcessor
from app.processing.ocr import OCRService
from app.processing.text_quality import TextQualityChecker


class PDFProcessor(BaseProcessor):
    def __init__(self):
        self.text_quality_checker = TextQualityChecker()
        self.ocr_service = OCRService()

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

            if self.text_quality_checker.is_suspicious(page_text):
                print("=" * 80)
                print("SUSPICIOUS TEXT DETECTED - USING OCR")

                pixmap = page.get_pixmap(
                    matrix=fitz.Matrix(2, 2),
                    alpha=False,
                )

                image = Image.frombytes(
                    "RGB",
                    [pixmap.width, pixmap.height],
                    pixmap.samples,
                )

                page_text = (
                    self.ocr_service.extract_text_from_image(
                        image
                    )
                )

                print("OCR TEXT:")
                print(repr(page_text[:500]))

            pages.append(page_text)

        page_count = len(document)
        document.close()

        text = "\n".join(pages)

        return text, page_count, pages