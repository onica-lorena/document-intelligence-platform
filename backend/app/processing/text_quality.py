import re


class TextQualityChecker:
    """
    Detects common signs of corrupted text extraction from PDFs.
    """

    CORRUPTED_PATTERNS = [
        r"ˆ",
        r"˘",
        r"[,][A-Za-z]",
        r"[A-Za-z],[A-Za-z]",
    ]

    def is_suspicious(self, text: str) -> bool:
        if not text:
            return True

        matches = 0

        for pattern in self.CORRUPTED_PATTERNS:
            matches += len(re.findall(pattern, text))

        return matches >= 2