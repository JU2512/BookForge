from pathlib import Path
from bs4 import BeautifulSoup


def validate_image_references(book_folder, reading_order):

    report = []

    ops_folder = book_folder / "OPS"

    for chapter in reading_order:

        chapter_file = ops_folder / chapter["file"]

        if not chapter_file.exists():
            continue

        with open(chapter_file, "r", encoding="utf-8") as f:

            soup = BeautifulSoup(f, "xml")

        issues = []

        for img in soup.find_all("img"):

            src = img.get("src")

            if not src:
                continue

            image_path = (chapter_file.parent / src).resolve()

            if not image_path.exists():

                issues.append({

                    "severity": "ERROR",

                    "rule": "Broken Image",

                    "message": f"{src} not found."

                })

        report.append({

            "chapter": chapter["file"],

            "issues": issues

        })

    return report