from pathlib import Path
from bs4 import BeautifulSoup


def validate_hyperlinks(book_folder, reading_order):

    report = []

    ops_folder = book_folder / "OPS"

    for chapter in reading_order:

        chapter_file = ops_folder / chapter["file"]

        if not chapter_file.exists():
            continue

        with open(chapter_file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "xml")

        issues = []

        for link in soup.find_all("a"):

            href = link.get("href")

            if not href:
                continue

            # Ignore external websites
            if href.startswith("http"):
                continue

            # Ignore mail links
            if href.startswith("mailto:"):
                continue

            file_name = href.split("#")[0]

            if file_name == "":
                continue

            target = (chapter_file.parent / file_name).resolve()

            if not target.exists():

                issues.append({

                    "severity": "ERROR",

                    "rule": "Hyperlink",

                    "message": f"{file_name} not found."

                })

        report.append({

            "chapter": chapter["file"],

            "issues": issues

        })

    return report