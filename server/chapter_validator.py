from server.rules import *


def validate_chapter(chapter):
    """
    Validate an individual EPUB chapter.

    Returns:
        {
            chapter,
            score,
            status,
            issues
        }
    """

    if not chapter:
        return {
            "chapter": "Unknown",
            "score": 0,
            "status": "ERROR",
            "issues": [
                {
                    "severity": "ERROR",
                    "rule": "Chapter",
                    "message": "Chapter data is missing."
                }
            ]
        }

    issues = []
    score = 100

    heading = chapter.get("heading", False)
    paragraphs = chapter.get("paragraphs", 0)
    word_count = chapter.get("word_count", 0)
    images = chapter.get("images", 0)
    chapter_name = chapter.get("chapter", "Unknown")

    # ---------------- Heading ----------------

    if HEADING_REQUIRED and not heading:

        issues.append({
            "severity": "WARNING",
            "rule": "Heading",
            "message": "Heading not found."
        })

        score -= 20

    # ---------------- Paragraphs ----------------

    if paragraphs < MIN_PARAGRAPHS:

        issues.append({
            "severity": "ERROR",
            "rule": "Paragraph",
            "message": "Chapter contains no paragraphs."
        })

        score -= 30

    # ---------------- Word Count ----------------

    if word_count < MIN_WORDS:

        issues.append({
            "severity": "WARNING",
            "rule": "Word Count",
            "message": f"Very little content ({word_count} words)."
        })

        score -= 15

    # ---------------- Images ----------------

    if images == 0:

        issues.append({
            "severity": "INFO",
            "rule": "Images",
            "message": "No images used."
        })

    # ---------------- Status ----------------

    if score == 100:
        status = "PASS"
    elif score >= 70:
        status = "WARNING"
    else:
        status = "ERROR"

    return {
        "chapter": chapter_name,
        "score": max(score, 0),
        "status": status,
        "issues": issues
    }