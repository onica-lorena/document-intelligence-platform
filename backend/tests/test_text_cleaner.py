from app.processing.cleaner import TextCleaner


def test_clean_normalizes_whitespace():
    cleaner = TextCleaner()

    text = "Hello     world\n\n\nThis is text."

    result = cleaner.clean(text)

    assert result == "Hello world\n\nThis is text."


def test_clean_normalizes_unicode():
    cleaner = TextCleaner()

    text = "ＡＢＣ"

    result = cleaner.clean(text)

    assert result == "ABC"


def test_clean_removes_leading_and_trailing_whitespace():
    cleaner = TextCleaner()

    text = "   Hello world   "

    result = cleaner.clean(text)

    assert result == "Hello world"


def test_clean_pages_preserves_page_positions():
    cleaner = TextCleaner()

    pages = [
        "Page 1",
        "",
        "Page 3",
    ]

    result = cleaner.clean_pages(pages)

    assert result == [
        "Page 1",
        "",
        "Page 3",
    ]