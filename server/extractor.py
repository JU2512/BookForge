from pathlib import Path
import zipfile
import shutil


EXTRACT_DIR = Path("server/storage/extracted")
EXTRACT_DIR.mkdir(parents=True, exist_ok=True)


def extract_epub(epub_path: Path) -> Path:
    """
    Extracts an EPUB file and returns
    the path to the extracted folder.
    """

    project_folder = EXTRACT_DIR / epub_path.stem

    # Remove old extraction if it exists
    if project_folder.exists():
        shutil.rmtree(project_folder)

    project_folder.mkdir(parents=True)

    with zipfile.ZipFile(epub_path, "r") as epub:
        epub.extractall(project_folder)

    return project_folder