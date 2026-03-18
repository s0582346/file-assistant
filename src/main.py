from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.document_reader import read_document, SUPPORTED_EXTENSIONS

app = FastAPI(title="Receipt Extractor")

RESOURCES_DIR = Path(__file__).parent.parent / "resources"


class ExtractRequest(BaseModel):
    file_name: str


@app.post("/extract")
def extract(request: ExtractRequest):
    """Extract structured data from a receipt or invoice in the resources folder."""
    file_path = RESOURCES_DIR / request.file_name

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: '{request.file_name}'")

    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: '{file_path.suffix}'")

    try:
        result = read_document(str(file_path))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return {"file": request.file_name, "data": result}
