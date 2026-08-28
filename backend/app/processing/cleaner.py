import re
import unicodedata


class TextCleaner:
    def clean(self, text: str) -> str:
        if not text:
            return ""

        text = unicodedata.normalize("NFKC", text)

        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        text = re.sub(r"[ \t]+", " ", text)

        text = re.sub(r"\n[ \t]+", "\n", text)

        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    def clean_pages(self, pages: list[str]) -> list[str]:
        return [self.clean(page) for page in pages]