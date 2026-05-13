from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.audit_log import AuditLog


async def log(
    session: AsyncSession,
    *,
    document_id: int,
    actor: str,
    action: str,
    from_status: str | None = None,
    to_status: str | None = None,
    note: str | None = None,
    extra: dict[str, Any] | None = None,
) -> AuditLog:
    entry = AuditLog(
        document_id=document_id,
        actor=actor,
        action=action,
        from_status=from_status,
        to_status=to_status,
        note=note,
        extra=extra,
    )
    session.add(entry)
    await session.flush()
    return entry


async def list_for_document(
    session: AsyncSession,
    document_id: int,
) -> list[AuditLog]:
    result = await session.execute(
        select(AuditLog)
        .where(AuditLog.document_id == document_id)
        .order_by(AuditLog.created_at.asc())
    )
    return list(result.scalars().all())
