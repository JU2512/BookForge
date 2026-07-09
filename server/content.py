from pathlib import Path
from bs4 import BeautifulSoup


def analyze_content(book_folder: Path, reading_order):

    report = []

    ops_folder = book_folder / "OPS"

    for chapter in reading_order:

        file_path = ops_folder / chapter["file"]

        chapter_report = {

            "chapter": chapter["file"],

            "exists": file_path.exists(),

            "heading": False,

            "paragraphs": 0,

            "images": 0,

            "word_count": 0

        }

        if file_path.exists():

            with open(file_path, "r", encoding="utf-8") as f:

                soup = BeautifulSoup(f, "xml")

            heading = soup.find(["h1", "h2", "h3"])

            chapter_report["heading"] = heading is not None

            paragraphs = soup.find_all("p")

            chapter_report["paragraphs"] = len(paragraphs)

            images = soup.find_all("img")

            chapter_report["images"] = len(images)

            text = soup.get_text(separator=" ")

            chapter_report["word_count"] = len(text.split())

        report.append(chapter_report)

    return report