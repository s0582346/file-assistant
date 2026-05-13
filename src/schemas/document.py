from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from src.models.document import DocumentStatus, DocumentType


class ExtractRequest(BaseModel):
    file_name: str


class DocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    file_path: str
    file_hash: str
    original_filename: str | None

    doc_type: DocumentType
    status: DocumentStatus

    doc_date: date | None
    due_date: date | None

    vendor: str | None
    category: str | None
    currency: str

    amount_gross: float | None
    amount_tax: float | None

    assigned_to: str | None
    decided_at: datetime | None
    decided_by: str | None
    decision_note: str | None

    raw_json: dict[str, Any] | None

    created_at: datetime
    updated_at: datetime


class ExtractResponse(BaseModel):
    document: DocumentRead
    extracted: dict[str, Any]
    deduplicated: bool
