import xml.etree.ElementTree as ET
from pathlib import Path


def validate_metadata(opf_path: Path):

    tree = ET.parse(opf_path)

    root = tree.getroot()

    namespace = {
        "dc": "http://purl.org/dc/elements/1.1/"
    }

    metadata = {}

    metadata["title"] = root.findtext(".//dc:title", default="", namespaces=namespace)

    metadata["creator"] = root.findtext(".//dc:creator", default="", namespaces=namespace)

    metadata["language"] = root.findtext(".//dc:language", default="", namespaces=namespace)

    metadata["publisher"] = root.findtext(".//dc:publisher", default="", namespaces=namespace)

    checks = []

    for field, value in metadata.items():

        if value.strip():

            checks.append({
                "field": field,
                "status": "PASS",
                "value": value
            })

        else:

            checks.append({
                "field": field,
                "status": "WARNING",
                "message": f"{field} is missing."
            })

    overall = "PASS"

    if any(c["status"] == "WARNING" for c in checks):
        overall = "WARNING"

    return {

        "module": "Metadata",

        "status": overall,

        "checks": checks

    }