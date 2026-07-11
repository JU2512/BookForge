import xml.etree.ElementTree as ET
from pathlib import Path


def parse_spine(opf_path: Path):
    """
    Parse the EPUB spine and return the reading order.
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

    spine = root.find("opf:spine", namespace)

    if spine is None:
        return []

    reading_order = []

    for item in spine.findall("opf:itemref", namespace):

        idref = item.attrib.get("idref")

        if idref:
            reading_order.append(idref)

    return reading_order