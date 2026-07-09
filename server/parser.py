from pathlib import Path
import xml.etree.ElementTree as ET



def find_opf(extracted_folder: Path) -> Path:
    """
    Reads META-INF/container.xml
    and returns the absolute path
    of the OPF file.
    """

    container_path = extracted_folder / "META-INF" / "container.xml"

    tree = ET.parse(container_path)
    root = tree.getroot()

    namespace = {
        "container": "urn:oasis:names:tc:opendocument:xmlns:container"
    }

    rootfile = root.find(
        ".//container:rootfile",
        namespace
    )

    opf_relative_path = rootfile.attrib["full-path"]

    return extracted_folder / opf_relative_path