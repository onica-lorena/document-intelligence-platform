from PIL import Image
import pytesseract


class OCRService:
    def __init__(self, language: str = "ron+eng"):
        self.language = language

    def extract_text_from_image(self, image: Image.Image) -> str:
        return pytesseract.image_to_string(
            image,
            lang=self.language,
        )