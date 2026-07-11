from pathlib import Path
from bs4 import BeautifulSoup


def analyze_content(book_folder: Path, reading_order):
    """
    Analyze chapter content.

    Extracts:
    - Heading presence
    - Paragraph count
    - Image count
    - Word count
    """

    report = []

    if not reading_order:
        return report

    ops_folder = book_folder / "OPS"

    for chapter in reading_order:

        chapter_name = chapter.get("file", "Unknown")
        file_path = ops_folder / chapter_name

        chapter_report = {
            "chapter": chapter_name,
            "exists": file_path.exists(),
            "heading": False,
            "paragraphs": 0,
            "images": 0,
            "word_count": 0
        }

        if not file_path.exists():
            report.append(chapter_report)
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "xml")

        except Exception:
            report.append(chapter_report)
            continue

        # First heading
        heading = soup.find(["h1", "h2", "h3"])
        chapter_report["heading"] = heading is not None

        # Paragraphs
        chapter_report["paragraphs"] = len(soup.find_all("p"))

        # Images
        chapter_report["images"] = len(soup.find_all("img"))

        # Word count
        text = soup.get_text(separator=" ", strip=True)
        chapter_report["word_count"] = len(text.split())

        report.append(chapter_report)

    return report