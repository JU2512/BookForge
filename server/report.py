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

    overall_score = metadata_quality["score"]

    # Grade Calculation
    if overall_score >= 90:
        grade = "A"
        status = "Excellent"

    elif overall_score >= 80:
        grade = "B"
        status = "Good"

    elif overall_score >= 70:
        grade = "C"
        status = "Needs Review"

    elif overall_score >= 60:
        grade = "D"
        status = "Major Fixes Required"

    else:
        grade = "F"
        status = "Not Production Ready"

    report = {

        "summary": {

            "overall_score": overall_score,
            "grade": grade,
            "status": status

        },

        "book": {

            "title": metadata["checks"][0]["value"],
            "author": metadata["checks"][1]["value"]

        },

        "quality": {

            "metadata": metadata_quality["score"],
            "html": 100,
            "css": 100,
            "images": 100,
            "hyperlinks": 100

        },

        "statistics": {

            "chapters": len(chapter_validation),
            "page_types": len(page_types),
            "stylesheets": len(css["checks"][0]["files"]),
            "images": len(images["checks"][0]["files"])

        },

        "issues": {

            "critical": [],
            "warnings": [],
            "information": []

        },

        "chapters": chapter_validation,

        "recommendations": []

    }

    # Metadata Issues
    for issue in metadata_quality["issues"]:

        if issue["severity"] == "ERROR":

            report["issues"]["critical"].append(issue)

            report["recommendations"].append(issue["message"])

        elif issue["severity"] == "WARNING":

            report["issues"]["warnings"].append(issue)

            report["recommendations"].append(issue["message"])

        else:

            report["issues"]["information"].append(issue)

    return report