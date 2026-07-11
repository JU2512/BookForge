from pathlib import Path
import xml.etree.ElementTree as ET


def find_opf(extracted_folder: Path) -> Path:
    """
    Locate the OPF file from META-INF/container.xml.

    Raises:
        FileNotFoundError
        ValueError
    """

    container_path = extracted_folder / "META-INF" / "container.xml"

    if not container_path.exists():
        raise FileNotFoundError(
            "container.xml not found inside EPUB."
        )

    try:
        tree = ET.parse(container_path)
        root = tree.getroot()

    except ET.ParseError:
        raise ValueError("Invalid container.xml.")

    namespace = {
        "container": "urn:oasis:names:tc:opendocument:xmlns:container"
    }

    rootfile = root.find(
        ".//container:rootfile",
        namespace
    )

    if rootfile is None:
        raise ValueError(
            "No rootfile entry found in container.xml."
        )

    opf_relative_path = rootfile.attrib.get("full-path")

    if not opf_relative_path:
        raise ValueError(
            "container.xml does not contain full-path."
        )

    opf_path = extracted_folder / opf_relative_path

    if not opf_path.exists():
        raise FileNotFoundError(
            f"OPF file not found: {opf_relative_path}"
        )

    return opf_path