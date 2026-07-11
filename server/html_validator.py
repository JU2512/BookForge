from pathlib import Path
from bs4 import BeautifulSoup


def validate_html(book_folder: Path, reading_order):
    """
    Validate HTML structure of every chapter in the EPUB.

    Returns a report for every chapter instead of stopping on the first one.
    """

    report = []

    if not reading_order:
        return report

    ops_folder = book_folder / "OPS"

    for chapter in reading_order:

        chapter_result = {
            "chapter": chapter.get("file", "Unknown"),
            "status": "PASS",
            "issues": []
        }

        chapter_file = ops_folder / chapter.get("file", "")

        # Missing chapter
        if not chapter_file.exists():

            chapter_result["status"] = "ERROR"

            chapter_result["issues"].append({
                "severity": "ERROR",
                "rule": "File",
                "message": "Chapter file not found."
            })

            report.append(chapter_result)
            continue

        try:

            with open(chapter_file, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "xml")

        except Exception as e:

            chapter_result["status"] = "ERROR"

            chapter_result["issues"].append({
                "severity": "ERROR",
                "rule": "Parser",
                "message": f"Unable to parse chapter: {str(e)}"
            })

            report.append(chapter_result)
            continue

        # ---------------- HTML ----------------

        if soup.find("html") is None:

            chapter_result["status"] = "ERROR"

            chapter_result["issues"].append({
                "severity": "ERROR",
                "rule": "HTML",
                "message": "Missing <html> tag."
            })

        # ---------------- HEAD ----------------

        if soup.find("head") is None:

            chapter_result["status"] = "ERROR"

            chapter_result["issues"].append({
                "severity": "ERROR",
                "rule": "HEAD",
                "message": "Missing <head> section."
            })

        # ---------------- BODY ----------------

        if soup.find("body") is None:

            chapter_result["status"] = "ERROR"

            chapter_result["issues"].append({
                "severity": "ERROR",
                "rule": "BODY",
                "message": "Missing <body> section."
            })

        # ---------------- H1 ----------------

        h1s = soup.find_all("h1")

        if len(h1s) > 1:

            chapter_result["issues"].append({
                "severity": "WARNING",
                "rule": "Heading",
                "message": "Multiple H1 headings found."
            })

        # ---------------- Empty headings ----------------

        for heading in soup.find_all(["h1", "h2", "h3"]):

            if heading.get_text(strip=True) == "":

                chapter_result["issues"].append({
                    "severity": "WARNING",
                    "rule": "Heading",
                    "message": "Empty heading detected."
                })

        # ---------------- Empty paragraphs ----------------

        for paragraph in soup.find_all("p"):

            if paragraph.get_text(strip=True) == "":

                chapter_result["issues"].append({
                    "severity": "WARNING",
                    "rule": "Paragraph",
                    "message": "Empty paragraph detected."
                })

        # ---------------- Images ----------------

        for image in soup.find_all("img"):

            if not image.get("alt"):

                chapter_result["issues"].append({
                    "severity": "WARNING",
                    "rule": "Accessibility",
                    "message": "Image missing ALT text."
                })

        report.append(chapter_result)

    return report