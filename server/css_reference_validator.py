from pathlib import Path
from bs4 import BeautifulSoup


def validate_css_references(book_folder: Path, reading_order):
    """
    Validate CSS references inside EPUB chapters.
    """

    report = []

    if not reading_order:
        return report

    ops_folder = book_folder / "OPS"

    for chapter in reading_order:

        chapter_file = ops_folder / chapter.get("file", "")

        chapter_report = {
            "chapter": chapter.get("file", "Unknown"),
            "status": "PASS",
            "issues": [],
            "statistics": {
                "stylesheets": 0,
                "broken_stylesheets": 0
            }
        }

        if not chapter_file.exists():

            chapter_report["status"] = "ERROR"

            chapter_report["issues"].append({
                "severity": "ERROR",
                "rule": "File",
                "message": "Chapter file not found."
            })

            report.append(chapter_report)
            continue

        try:

            with open(chapter_file, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "xml")

        except Exception as e:

            chapter_report["status"] = "ERROR"

            chapter_report["issues"].append({
                "severity": "ERROR",
                "rule": "Parser",
                "message": f"Unable to parse chapter: {e}"
            })

            report.append(chapter_report)
            continue

        links = soup.find_all("link")

        if not links:

            chapter_report["issues"].append({
                "severity": "WARNING",
                "rule": "Stylesheet",
                "message": "No stylesheet linked."
            })

        for link in links:

            chapter_report["statistics"]["stylesheets"] += 1

            href = link.get("href")
            rel = link.get("rel")

            if not href:

                chapter_report["issues"].append({
                    "severity": "WARNING",
                    "rule": "Stylesheet",
                    "message": "Stylesheet href is missing."
                })
                continue

            css_path = (chapter_file.parent / href).resolve()

            if not css_path.exists():

                chapter_report["status"] = "ERROR"
                chapter_report["statistics"]["broken_stylesheets"] += 1

                chapter_report["issues"].append({
                    "severity": "ERROR",
                    "rule": "Stylesheet",
                    "message": f"Missing stylesheet: {href}"
                })

            if rel != ["stylesheet"] and rel != "stylesheet":

                chapter_report["issues"].append({
                    "severity": "WARNING",
                    "rule": "Stylesheet",
                    "message": "Missing rel='stylesheet'."
                })

        report.append(chapter_report)

    return report