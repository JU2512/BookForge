REQUIRED_FIELDS = {
    "title": 20,
    "creator": 20,
    "language": 15,
    "publisher": 15,
    "identifier": 20,
    "date": 10
}


def validate_metadata(metadata_report):
    """
    Validate EPUB metadata and calculate metadata quality score.

    Handles missing metadata safely without raising KeyError.
    """

    score = 100
    issues = []
    found_fields = {}

    # Read metadata safely
    for item in metadata_report.get("checks", []):

        field = item.get("field")

        if not field:
            continue

        # Missing metadata entries may not contain "value"
        found_fields[field] = item.get("value", "")

        # Preserve existing metadata errors if present
        if item.get("status") == "ERROR":
            issues.append({
                "severity": "ERROR",
                "field": field,
                "message": item.get(
                    "message",
                    f"{field} is missing."
                )
            })

    # Check required fields
    for field, weight in REQUIRED_FIELDS.items():

        value = found_fields.get(field, "")

        if not value:

            # Avoid duplicate errors
            already_exists = any(
                issue["field"] == field
                for issue in issues
            )

            if not already_exists:
                issues.append({
                    "severity": "ERROR",
                    "field": field,
                    "message": f"{field} is missing."
                })

            score -= weight

    return {
        "score": max(score, 0),
        "issues": issues
    }