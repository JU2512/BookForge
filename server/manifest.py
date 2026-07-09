import xml.etree.ElementTree as ET
from pathlib import Path


def parse_manifest(opf_path: Path):

    tree = ET.parse(opf_path)

    root = tree.getroot()

    namespace = {
        "opf": "http://www.idpf.org/2007/opf"
    }

    manifest = root.find("opf:manifest", namespace)

    items = []

    for item in manifest.findall("opf:item", namespace):

        items.append({

            "id": item.attrib.get("id"),

            "href": item.attrib.get("href"),

            "media_type": item.attrib.get("media-type")

        })

    return items