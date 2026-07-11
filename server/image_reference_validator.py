from pathlib import Path
from bs4 import BeautifulSoup


def validate_image_references(book_folder: Path, reading_order):
    """
    Validate image references inside EPUB chapters.

    Checks:
    - Missing image files
    - Invalid image references

    Returns a validation report for every chapter.
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
                "images": 0,
                "broken_images": 0
            }
        }

        # Missing chapter file
        if not chapter_file.exists():

            chapter_report["status"] = "ERROR"

            chapter_report["issues"].append({
                "severity": "ERROR",
                "rule": "File",
                "message": "Chapter file not found."
            })

            report.append(chapter_report)
            continue

        # Parse chapter
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

        # Validate images
        for img in soup.find_all("img"):

            chapter_report["statistics"]["images"] += 1

            src = img.get("src")

            if not src:

                chapter_report["issues"].append({
                    "severity": "WARNING",
                    "rule": "Image",
                    "message": "Image source (src) is missing."
                })

                continue

            image_path = (chapter_file.parent / src).resolve()

            if not image_path.exists():

                chapter_report["status"] = "ERROR"

                chapter_report["statistics"]["broken_images"] += 1

                chapter_report["issues"].append({
                    "severity": "ERROR",
                    "rule": "Broken Image",
                    "message": f"Missing image: {src}"
                })

        report.append(chapter_report)

    return report