import fitz
import pytest

from app.processing.pdf_processor import PDFProcessor


@pytest.mark.anyio
async def test_extract_text_from_pdf(tmp_path):
    pdf_path = tmp_path / "test.pdf"

    document = fitz.open()

    page1 = document.new_page()
    page1.insert_text((50, 50), "This is page one.")

    page2 = document.new_page()
    page2.insert_text((50, 50), "This is page two.")

    document.save(pdf_path)
    document.close()

    processor = PDFProcessor()

    text, page_count, pages = await processor.extract_text(
        str(pdf_path)
    )

    assert page_count == 2
    assert len(pages) == 2

    assert "This is page one." in pages[0]
    assert "This is page two." in pages[1]

    assert "This is page one." in text
    assert "This is page two." in text