from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException
from server.extractor import extract_epub
from server.parser import find_opf
from server.metadata import validate_metadata
from server.manifest import parse_manifest
from server.validator import validate_css
from server.validator import validate_css, validate_images
from server.spine import parse_spine
from server.resolver import resolve_spine
from server.content import analyze_content
from server.chapter_validator import validate_chapter
from server.html_validator import validate_html
from server.report import generate_report
from server.page_classifier import classify_pages
from server.image_reference_validator import validate_image_references
from server.css_reference_validator import validate_css_references
from server.hyperlink_validator import validate_hyperlinks
from server.metadata_validator import validate_metadata as validate_metadata_quality

app = FastAPI(
    title="BookForge API",
    description="API for EPUB inspection and validation",
    version="1.0.0"
)

UPLOAD_DIR = Path("server/storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "Welcome to BookForge API 🚀"
    }


@app.post("/analyze")
async def analyze_book(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".epub"):
        raise HTTPException(
            status_code=400,
            detail="Only EPUB files are supported."
        )

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
        extracted_folder = extract_epub(file_path)
        opf_path = find_opf(extracted_folder)
        metadata_report = validate_metadata(opf_path)
        manifest = parse_manifest(opf_path)
        css_report = validate_css(manifest)
        image_report = validate_images(manifest)
        spine = parse_spine(opf_path)
        reading_order = resolve_spine(manifest, spine)
        book_folder = opf_path.parent.parent
        page_types = classify_pages(
                book_folder,
                reading_order
            )
        image_reference_report = validate_image_references(
                book_folder,
                reading_order
            )
        
        css_reference_report = validate_css_references(
                    book_folder,
                    reading_order
                )
        
        hyperlink_report = validate_hyperlinks(
                book_folder,
                reading_order
            )
        
        content_report = analyze_content(book_folder, reading_order)
        chapter_reports = []

        for chapter in content_report:
            chapter_reports.append(
         validate_chapter(chapter)
        )
            
        html_report = validate_html(
            book_folder,
            reading_order
        )
        metadata_report = validate_metadata(opf_path)

        metadata_quality = validate_metadata_quality(metadata_report)

        final_report = generate_report(

            metadata_report,
            metadata_quality,
            css_report,
            css_reference_report,
            image_report,
            image_reference_report,
            hyperlink_report,
            html_report,
            chapter_reports,
            page_types

        )

        return final_report