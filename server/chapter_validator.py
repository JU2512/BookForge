from server.rules import *
from server.rules import HEADING_REQUIRED
from server.rules import MIN_PARAGRAPHS
from server.rules import MIN_WORDS


def validate_chapter(chapter):

    issues = []

    score = 100

    if HEADING_REQUIRED and not chapter["heading"]:

        issues.append({

            "severity": "WARNING",

            "rule": "Heading",

            "message": "Heading not found."

        })

        score -= 20

    if chapter["paragraphs"] < MIN_PARAGRAPHS:

        issues.append({

            "severity": "ERROR",

            "rule": "Paragraph",

            "message": "Chapter contains no paragraphs."

        })

        score -= 30

    if chapter["word_count"] < MIN_WORDS:

        issues.append({

            "severity": "WARNING",

            "rule": "Word Count",

            "message": f"Very little content ({chapter['word_count']} words)."

        })

        score -= 15

    if chapter["images"] == 0:

        issues.append({

            "severity": "INFO",

            "rule": "Images",

            "message": "No images used."

        })

    return {

        "chapter": chapter["chapter"],

        "score": max(score, 0),

        "status": "PASS" if score == 100 else "WARNING" if score >= 70 else "ERROR",

        "issues": issues

    }