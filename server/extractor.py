from pathlib import Path
import zipfile
import shutil


EXTRACT_DIR = Path("server/storage/extracted")
EXTRACT_DIR.mkdir(parents=True, exist_ok=True)


def extract_epub(epub_path: Path) -> Path:
    """
    Extract an EPUB archive and return the extracted folder.

    Raises:
        FileNotFoundError
        ValueError (if file is not a valid EPUB/ZIP)
    """

    if not epub_path.exists():
        raise FileNotFoundError(f"EPUB not found: {epub_path}")

    project_folder = EXTRACT_DIR / epub_path.stem

    # Remove previous extraction
    if project_folder.exists():
        try:
            shutil.rmtree(project_folder)
        except Exception:
            pass

    project_folder.mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(epub_path, "r") as epub:
            epub.extractall(project_folder)

    except zipfile.BadZipFile:
        raise ValueError("Uploaded file is not a valid EPUB archive.")

    return project_folder