from __future__ import annotations

from pydantic import BaseModel, EmailStr


class ApprovalAction(BaseModel):
    actor: EmailStr
    note: str | None = None
