from __future__ import annotations

from sqlalchemy import Boolean, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class ApprovalRule(Base):
    __tablename__ = "approval_rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=100)

    doc_type: Mapped[str | None] = mapped_column(String(32))
    category: Mapped[str | None] = mapped_column(String(128))
    vendor_pattern: Mapped[str | None] = mapped_column(String(255))

    amount_min: Mapped[float | None] = mapped_column(Numeric(14, 2))
    amount_max: Mapped[float | None] = mapped_column(Numeric(14, 2))

    approver_email: Mapped[str] = mapped_column(String(255), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
