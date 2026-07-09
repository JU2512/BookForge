from pathlib import Path
from bs4 import BeautifulSoup


def classify_pages(book_folder: Path, reading_order):

    ops_folder = book_folder / "OPS"

    pages = []

    for page in reading_order:

        page_type = "CONTENT"

        filename = page["file"].lower()

        file_path = ops_folder / page["file"]

        if "cover" in filename:

            page_type = "COVER"

        elif "title" in filename:

            page_type = "TITLE"

        elif "toc" in filename or "nav" in filename:

            page_type = "TOC"

        elif "copyright" in filename:

            page_type = "COPYRIGHT"

        elif "index" in filename:

            page_type = "INDEX"

        elif "appendix" in filename:

            page_type = "APPENDIX"

        elif "ending" in filename:

            page_type = "BACK_MATTER"

        # Improve classification using the XHTML content
        if file_path.exists():

            with open(file_path, "r", encoding="utf-8") as f:

                soup = BeautifulSoup(f, "xml")

            nav = soup.find("nav")

            if nav and nav.get("epub:type") == "toc":
                page_type = "TOC"

        pages.append({

            "id": page["id"],

            "file": page["file"],

            "page_type": page_type

        })

    return pages