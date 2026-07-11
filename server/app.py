from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from server.extractor import extract_epub
from server.parser import find_opf
from server.metadata import validate_metadata
from server.manifest import parse_manifest
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
from fastapi.responses import FileResponse
from server.pdf_report import generate_pdf

app = FastAPI(
    title="BookForge API",
    description="API for EPUB inspection and validation",
    version="1.0.0"
)

# -----------------------------
# CORS CONFIGURATION
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("server/storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

EXPORT_DIR = Path("server/storage/reports")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

# Stores the most recent analysis report
LAST_REPORT = None

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

    content_report = analyze_content(
        book_folder,
        reading_order
    )

    chapter_reports = []

    for chapter in content_report:
        chapter_reports.append(
            validate_chapter(chapter)
        )

    html_report = validate_html(
        book_folder,
        reading_order
    )

    metadata_quality = validate_metadata_quality(
        metadata_report
    )

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

    global LAST_REPORT
    LAST_REPORT = final_report

    return final_report

@app.get("/export/pdf")
def export_pdf():

    global LAST_REPORT

    if LAST_REPORT is None:
        raise HTTPException(
            status_code=400,
            detail="Analyze an EPUB before exporting a PDF."
        )

    pdf_path = EXPORT_DIR / "BookForge_Report.pdf"

    generate_pdf(
        LAST_REPORT,
        pdf_path
    )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename="BookForge_Report.pdf"
    )