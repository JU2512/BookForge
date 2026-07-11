import xml.etree.ElementTree as ET
from pathlib import Path


def parse_manifest(opf_path: Path):
    """
    Parse the EPUB manifest (content.opf).

    Returns a list of manifest items. If the OPF is malformed or the
    manifest is missing, an empty list is returned instead of raising
    an exception.
    """

    if not opf_path.exists():
        return []

    try:
        tree = ET.parse(opf_path)
        root = tree.getroot()

    except ET.ParseError:
        return []

    except Exception:
        return []

    namespace = {
        "opf": "http://www.idpf.org/2007/opf"
    }

    manifest = root.find("opf:manifest", namespace)

    if manifest is None:
        return []

    items = []

    for item in manifest.findall("opf:item", namespace):

        items.append({

            "id": item.attrib.get("id", ""),

            "href": item.attrib.get("href", ""),

            "media_type": item.attrib.get("media-type", "")

        })

    return items