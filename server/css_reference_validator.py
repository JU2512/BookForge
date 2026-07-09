from pathlib import Path
from bs4 import BeautifulSoup


def validate_css_references(book_folder, reading_order):

    report = []

    ops_folder = book_folder / "OPS"

    for chapter in reading_order:

        chapter_file = ops_folder / chapter["file"]

        if not chapter_file.exists():
            continue

        with open(chapter_file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "xml")

        issues = []

        links = soup.find_all("link")

        if len(links) == 0:

            issues.append({

                "severity": "WARNING",

                "rule": "Stylesheet",

                "message": "No stylesheet linked."

            })

        for link in links:

            href = link.get("href")

            rel = link.get("rel")

            if href is None:
                continue

            css_path = (chapter_file.parent / href).resolve()

            if not css_path.exists():

                issues.append({

                    "severity": "ERROR",

                    "rule": "Stylesheet",

                    "message": f"{href} not found."

                })

            if rel != ["stylesheet"] and rel != "stylesheet":

                issues.append({

                    "severity": "WARNING",

                    "rule": "Stylesheet",

                    "message": "Missing rel='stylesheet'."

                })

        report.append({

            "chapter": chapter["file"],

            "issues": issues

        })

    return report