from pathlib import Path
from bs4 import BeautifulSoup


def classify_pages(book_folder: Path, reading_order):
    """
    Classify EPUB pages based on filename and XHTML content.
    """

    pages = []

    if not reading_order:
        return pages

    ops_folder = book_folder / "OPS"

    for page in reading_order:

        file_name = page.get("file", "")
        file_path = ops_folder / file_name

        filename = file_name.lower()

        page_type = "CONTENT"

        if "cover" in filename:
            page_type = "COVER"

        elif "title" in filename:
            page_type = "TITLE"

        elif "toc" in filename or "nav" in filename:
            page_type = "TOC"

        elif "copyright" in filename:
            page_type = "COPYRIGHT"

        elif "preface" in filename:
            page_type = "PREFACE"

        elif "foreword" in filename:
            page_type = "FOREWORD"

        elif "glossary" in filename:
            page_type = "GLOSSARY"

        elif "bibliography" in filename:
            page_type = "BIBLIOGRAPHY"

        elif "appendix" in filename:
            page_type = "APPENDIX"

        elif "index" in filename:
            page_type = "INDEX"

        elif "ending" in filename or "back" in filename:
            page_type = "BACK_MATTER"

        if file_path.exists():

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    soup = BeautifulSoup(f, "xml")

                nav = soup.find("nav")

                if nav and nav.get("epub:type") == "toc":
                    page_type = "TOC"

            except Exception:
                # Keep filename-based classification
                pass

        pages.append({
            "id": page.get("id", ""),
            "file": file_name,
            "page_type": page_type
        })

    return pages