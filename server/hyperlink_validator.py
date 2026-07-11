from pathlib import Path
from bs4 import BeautifulSoup


def validate_hyperlinks(book_folder: Path, reading_order):
    """
    Validate internal hyperlinks inside EPUB chapters.

    Checks:
    - Missing href
    - Broken internal links
    - Ignores external (http/https)
    - Ignores mailto links

    Returns a report for every chapter.
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
                "total_links": 0,
                "broken_links": 0
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
                "message": f"Unable to parse chapter: {str(e)}"
            })

            report.append(chapter_report)
            continue

        for link in soup.find_all("a"):

            chapter_report["statistics"]["total_links"] += 1

            href = link.get("href")

            if not href:

                chapter_report["issues"].append({
                    "severity": "WARNING",
                    "rule": "Hyperlink",
                    "message": "Empty hyperlink detected."
                })

                continue

            # Ignore external URLs
            if href.startswith(("http://", "https://")):
                continue

            # Ignore email links
            if href.startswith("mailto:"):
                continue

            file_name = href.split("#")[0]

            # Anchor within same page
            if file_name == "":
                continue

            target = (chapter_file.parent / file_name).resolve()

            if not target.exists():

                chapter_report["status"] = "ERROR"

                chapter_report["statistics"]["broken_links"] += 1

                chapter_report["issues"].append({
                    "severity": "ERROR",
                    "rule": "Hyperlink",
                    "message": f"Broken link: {file_name}"
                })

        report.append(chapter_report)

    return report