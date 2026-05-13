from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.db.session import get_db
from src.models.document import DocumentStatus
from src.repositories import documents as documents_repo
from src.schemas.document import DocumentRead, ExtractRequest, ExtractResponse
from src.services.document_reader import SUPPORTED_EXTENSIONS
from src.services.ingest import ingest_file

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/extract", response_model=ExtractResponse)
async def extract(
    request: ExtractRequest,
    session: AsyncSession = Depends(get_db),
):
    """Extract structured data from a file in the resources folder and persist it."""
    file_path = settings.resources_dir / request.file_name

    if not file_path.exists():
        raise HTTPException(404, f"File not found: '{request.file_name}'")
    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise HTTPException(400, f"Unsupported file type: '{file_path.suffix}'")

    try:
        document, raw, deduplicated = await ingest_file(session, file_path)
    except ValueError as e:
        raise HTTPException(422, str(e))

    await session.commit()
    await session.refresh(document)

    return ExtractResponse(
        document=DocumentRead.model_validate(document),
        extracted=raw,
        deduplicated=deduplicated,
    )


@router.get("/{document_id}", response_model=DocumentRead)
async def get_document(
    document_id: int,
    session: AsyncSession = Depends(get_db),
):
    document = await documents_repo.get_by_id(session, document_id)
    if document is None:
        raise HTTPException(404, f"Document {document_id} not found")
    return DocumentRead.model_validate(document)


@router.get("", response_model=list[DocumentRead])
async def list_documents(
    status: DocumentStatus = DocumentStatus.pending_review,
    limit: int = 100,
    session: AsyncSession = Depends(get_db),
):
    docs = await documents_repo.list_by_status(session, status, limit=limit)
    return [DocumentRead.model_validate(d) for d in docs]
