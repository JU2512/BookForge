import xml.etree.ElementTree as ET
from pathlib import Path


def parse_spine(opf_path: Path):

    tree = ET.parse(opf_path)

    root = tree.getroot()

    namespace = {
        "opf": "http://www.idpf.org/2007/opf"
    }

    spine = root.find("opf:spine", namespace)

    reading_order = []

    for item in spine.findall("opf:itemref", namespace):

        reading_order.append(
            item.attrib.get("idref")
        )

    return reading_order