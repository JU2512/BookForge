import xml.etree.ElementTree as ET
from pathlib import Path


def validate_metadata(opf_path: Path):
    """
    Extract and validate EPUB metadata.

    Returns a consistent metadata report that is consumed by
    metadata_validator.py.
    """

    if not opf_path.exists():

        return {
            "module": "Metadata",
            "status": "ERROR",
            "checks": []
        }

    try:

        tree = ET.parse(opf_path)
        root = tree.getroot()

    except ET.ParseError:

        return {
            "module": "Metadata",
            "status": "ERROR",
            "checks": []
        }

    namespace = {
        "dc": "http://purl.org/dc/elements/1.1/"
    }

    metadata = {

        "title": root.findtext(
            ".//dc:title",
            default="",
            namespaces=namespace
        ),

        "creator": root.findtext(
            ".//dc:creator",
            default="",
            namespaces=namespace
        ),

        "language": root.findtext(
            ".//dc:language",
            default="",
            namespaces=namespace
        ),

        "publisher": root.findtext(
            ".//dc:publisher",
            default="",
            namespaces=namespace
        ),

        "identifier": root.findtext(
            ".//dc:identifier",
            default="",
            namespaces=namespace
        ),

        "date": root.findtext(
            ".//dc:date",
            default="",
            namespaces=namespace
        )

    }

    checks = []

    overall = "PASS"

    for field, value in metadata.items():

        value = value.strip()

        if value:

            checks.append({
                "field": field,
                "status": "PASS",
                "value": value
            })

        else:

            overall = "WARNING"

            checks.append({
                "field": field,
                "status": "WARNING",
                "message": f"{field} is missing."
            })

    return {

        "module": "Metadata",

        "status": overall,

        "checks": checks

    }