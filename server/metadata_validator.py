REQUIRED_FIELDS = {

    "title": 20,

    "creator": 20,

    "language": 15,

    "publisher": 15,

    "identifier": 20,

    "date": 10

}


def validate_metadata(metadata_report):

    score = 100

    issues = []

    found_fields = {}

    for item in metadata_report["checks"]:

        found_fields[item["field"]] = item["value"]

    for field, weight in REQUIRED_FIELDS.items():

        value = found_fields.get(field)

        if value is None or value == "":

            score -= weight

            issues.append({

                "severity": "ERROR",

                "field": field,

                "message": f"{field} is missing."

            })

    return {

        "score": max(score, 0),

        "issues": issues

    }