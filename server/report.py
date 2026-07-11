"""
BookForge Report Generator

This module combines the outputs of every validator
and produces the final JSON consumed by the frontend.
"""


# ----------------------------------------------------
# Generic Helpers
# ----------------------------------------------------

def clamp_score(score):
    """Keep score between 0 and 100."""
    return max(0, min(100, round(score)))


# ----------------------------------------------------
# Grade
# ----------------------------------------------------

def calculate_grade(score):

    if score >= 90:
        return "A", "Excellent"

    elif score >= 80:
        return "B", "Good"

    elif score >= 70:
        return "C", "Needs Review"

    elif score >= 60:
        return "D", "Major Fixes Required"

    return "F", "Not Production Ready"


# ----------------------------------------------------
# Metadata Extraction
# ----------------------------------------------------

def extract_metadata(metadata):

    metadata_map = {}

    for item in metadata.get("checks", []):

        field = item.get("field")

        if field:
            metadata_map[field] = item.get("value", "")

    return {
        "title": metadata_map.get("title", "Unknown"),
        "author": metadata_map.get("creator", "Unknown"),
        "language": metadata_map.get("language", "Unknown"),
        "publisher": metadata_map.get("publisher", "Unknown"),
        "identifier": metadata_map.get("identifier", ""),
        "date": metadata_map.get("date", "")
    }


# ----------------------------------------------------
# Count Manifest Files
# ----------------------------------------------------

def count_stylesheets(css):

    checks = css.get("checks", [])

    if not checks:
        return 0

    return len(checks[0].get("files", []))


def count_images(images):

    checks = images.get("checks", [])

    if not checks:
        return 0

    return len(checks[0].get("files", []))


# ----------------------------------------------------
# Generic Validator Score
# ----------------------------------------------------

def calculate_validator_score(report):

    """
    Converts validator issues into a score.

    ERROR   -> -10
    WARNING -> -5
    INFO    -> 0
    """

    score = 100

    if not report:
        return score

    for chapter in report:

        for issue in chapter.get("issues", []):

            severity = issue.get("severity", "").upper()

            if severity == "ERROR":
                score -= 10

            elif severity == "WARNING":
                score -= 5

    return clamp_score(score)


# ----------------------------------------------------
# Chapter Average
# ----------------------------------------------------

def calculate_chapter_score(chapters):

    if not chapters:
        return 100

    total = 0

    for chapter in chapters:
        total += chapter.get("score", 100)

    return clamp_score(total / len(chapters))


# ----------------------------------------------------
# Overall Score
# ----------------------------------------------------

def calculate_overall_score(
    metadata_score,
    html_score,
    css_score,
    image_score,
    hyperlink_score,
    chapter_score
):

    overall = (

        metadata_score * 0.20 +

        html_score * 0.20 +

        css_score * 0.15 +

        image_score * 0.15 +

        hyperlink_score * 0.15 +

        chapter_score * 0.15

    )

    return clamp_score(overall)

# ----------------------------------------------------
# Issue Aggregation
# ----------------------------------------------------

def aggregate_issues(
    metadata_quality,
    html_validation,
    css_reference,
    image_reference,
    hyperlinks,
    chapter_validation
):
    """
    Merge issues from every validator into a single structure.
    """

    issues = {
        "critical": [],
        "warnings": [],
        "information": []
    }

    # ---------------- Metadata ----------------

    for issue in metadata_quality.get("issues", []):

        severity = issue.get("severity", "").upper()

        if severity == "ERROR":
            issues["critical"].append(issue)

        elif severity == "WARNING":
            issues["warnings"].append(issue)

        else:
            issues["information"].append(issue)

    # ---------------- Generic Validators ----------------

    validator_reports = [
        html_validation,
        css_reference,
        image_reference,
        hyperlinks
    ]

    for report in validator_reports:

        for chapter in report:

            for issue in chapter.get("issues", []):

                severity = issue.get("severity", "").upper()

                if severity == "ERROR":
                    issues["critical"].append(issue)

                elif severity == "WARNING":
                    issues["warnings"].append(issue)

                else:
                    issues["information"].append(issue)

    # ---------------- Chapter Validation ----------------

    for chapter in chapter_validation:

        for issue in chapter.get("issues", []):

            severity = issue.get("severity", "").upper()

            if severity == "ERROR":
                issues["critical"].append(issue)

            elif severity == "WARNING":
                issues["warnings"].append(issue)

            else:
                issues["information"].append(issue)

    return issues


# ----------------------------------------------------
# Recommendations
# ----------------------------------------------------

def generate_recommendations(issues):
    """
    Generate unique recommendations from issues.
    """

    recommendations = []
    seen = set()

    for category in issues.values():

        for issue in category:

            message = issue.get("message", "").strip()

            if message and message not in seen:

                recommendations.append(message)

                seen.add(message)

    return recommendations


# ----------------------------------------------------
# Quality Report
# ----------------------------------------------------

def build_quality_report(
    metadata_quality,
    html_validation,
    css_reference,
    image_reference,
    hyperlinks,
    chapter_validation
):

    metadata_score = metadata_quality.get("score", 0)

    html_score = calculate_validator_score(html_validation)

    css_score = calculate_validator_score(css_reference)

    image_score = calculate_validator_score(image_reference)

    hyperlink_score = calculate_validator_score(hyperlinks)

    chapter_score = calculate_chapter_score(chapter_validation)

    return {

        "metadata": metadata_score,

        "html": html_score,

        "css": css_score,

        "images": image_score,

        "hyperlinks": hyperlink_score,

        "chapters": chapter_score

    }


# ----------------------------------------------------
# Statistics
# ----------------------------------------------------

def build_statistics(
    chapter_validation,
    page_types,
    css,
    images,
    hyperlinks
):

    hyperlink_count = 0

    for chapter in hyperlinks:

        stats = chapter.get("statistics", {})

        hyperlink_count += stats.get("total_links", 0)

    return {

        "chapters": len(chapter_validation),

        "page_types": len(page_types),

        "stylesheets": count_stylesheets(css),

        "images": count_images(images),

        "hyperlinks": hyperlink_count

    }


def generate_report(
    metadata,
    metadata_quality,
    css,
    css_reference,
    images,
    image_reference,
    hyperlinks,
    html_validation,
    chapter_validation,
    page_types
):

    # ----------------------------
    # Metadata
    # ----------------------------

    book = extract_metadata(metadata)

    # ----------------------------
    # Quality Scores
    # ----------------------------

    quality = build_quality_report(
        metadata_quality,
        html_validation,
        css_reference,
        image_reference,
        hyperlinks,
        chapter_validation
    )

    # ----------------------------
    # Overall Score
    # ----------------------------

    overall_score = calculate_overall_score(
        quality["metadata"],
        quality["html"],
        quality["css"],
        quality["images"],
        quality["hyperlinks"],
        calculate_chapter_score(chapter_validation)
    )

    grade, status = calculate_grade(overall_score)

    # ----------------------------
    # Statistics
    # ----------------------------

    statistics = build_statistics(
        chapter_validation,
        page_types,
        css,
        images,
        hyperlinks
    )

    # ----------------------------
    # Issues
    # ----------------------------

    issues = aggregate_issues(
        metadata_quality,
        html_validation,
        css_reference,
        image_reference,
        hyperlinks,
        chapter_validation
    )

    # ----------------------------
    # Recommendations
    # ----------------------------

    recommendations = generate_recommendations(
        issues
    )

    # ----------------------------
    # Final Report
    # ----------------------------

    return {

        "summary": {

            "overall_score": overall_score,

            "grade": grade,

            "status": status

        },

        "book": {

            "title": book["title"],

            "author": book["author"]

        },

        "quality": {

            "metadata": quality["metadata"],

            "html": quality["html"],

            "css": quality["css"],

            "images": quality["images"],

            "hyperlinks": quality["hyperlinks"]

        },

        "statistics": statistics,

        "issues": issues,

        "chapters": chapter_validation,

        "recommendations": recommendations

    }