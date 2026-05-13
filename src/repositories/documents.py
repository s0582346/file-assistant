from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.document import Document, DocumentStatus, DocumentType


async def get_by_id(session: AsyncSession, document_id: int) -> Document | None:
    return await session.get(Document, document_id)


async def get_by_hash(session: AsyncSession, file_hash: str) -> Document | None:
    result = await session.execute(
        select(Document).where(Document.file_hash == file_hash)
    )
    return result.scalar_one_or_none()


async def list_by_status(
    session: AsyncSession,
    status: DocumentStatus,
    limit: int = 100,
) -> list[Document]:
    result = await session.execute(
        select(Document)
        .where(Document.status == status)
        .order_by(Document.due_date.asc().nullslast(), Document.created_at.desc())
        .limit(limit)
    )
    return list(result.scalars().all())


async def create(
    session: AsyncSession,
    *,
    file_path: str,
    file_hash: str,
    original_filename: str | None,
    doc_type: DocumentType,
    raw_json: dict[str, Any] | None,
    doc_date=None,
    due_date=None,
    vendor: str | None = None,
    category: str | None = None,
    currency: str = "EUR",
    amount_gross: float | None = None,
    amount_tax: float | None = None,
) -> Document:
    document = Document(
        file_path=file_path,
        file_hash=file_hash,
        original_filename=original_filename,
        doc_type=doc_type,
        raw_json=raw_json,
        doc_date=doc_date,
        due_date=due_date,
        vendor=vendor,
        category=category,
        currency=currency,
        amount_gross=amount_gross,
        amount_tax=amount_tax,
    )
    session.add(document)
    await session.flush()
    return document


async def update_status(
    session: AsyncSession,
    document: Document,
    *,
    new_status: DocumentStatus,
    decided_by: str | None = None,
    decision_note: str | None = None,
) -> Document:
    from datetime import datetime, timezone

    document.status = new_status
    document.decided_by = decided_by
    document.decision_note = decision_note
    document.decided_at = datetime.now(timezone.utc)
    await session.flush()
    return document
