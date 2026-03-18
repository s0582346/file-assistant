from pathlib import Path

import pdfplumber

from src.extractor import extract_from_text, extract_from_image

SUPPORTED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
SUPPORTED_PDF_EXTENSIONS = {".pdf"}
SUPPORTED_EXTENSIONS = SUPPORTED_IMAGE_EXTENSIONS | SUPPORTED_PDF_EXTENSIONS


def read_pdf(file_path: str) -> dict:
    """Extract text from a PDF and return structured receipt data."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    if not text.strip():
        raise ValueError(f"No text could be extracted from '{file_path}'. It may be a scanned/image-based PDF.")

    return extract_from_text(text)


def read_image(file_path: str) -> dict:
    """Extract receipt data from an image file via Claude vision."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: '{file_path}'")
    if path.suffix.lower() not in SUPPORTED_IMAGE_EXTENSIONS:
        raise ValueError(f"Unsupported image format: '{path.suffix}'")

    return extract_from_image(file_path)


def get_document_type(file_path: str) -> str:
    """Return 'pdf', 'image', or raise ValueError for unsupported types."""
    ext = Path(file_path).suffix.lower()
    if ext in SUPPORTED_PDF_EXTENSIONS:
        return "pdf"
    if ext in SUPPORTED_IMAGE_EXTENSIONS:
        return "image"
    raise ValueError(f"Unsupported file type: '{ext}'")


def read_document(file_path: str) -> dict:
    """Read any supported document and return structured receipt data."""
    doc_type = get_document_type(file_path)
    if doc_type == "pdf":
        return read_pdf(file_path)
    return read_image(file_path)


def list_documents(directory: str) -> list[str]:
    """List all supported document files in a directory."""
    dir_path = Path(directory)
    if not dir_path.is_dir():
        raise NotADirectoryError(f"Not a directory: '{directory}'")

    files = [
        str(f) for f in sorted(dir_path.iterdir())
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    return files