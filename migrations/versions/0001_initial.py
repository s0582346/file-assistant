"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-05-13

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


document_type_enum = postgresql.ENUM(
    "invoice", "receipt", "payslip", "unknown",
    name="document_type",
    create_type=False,
)
document_status_enum = postgresql.ENUM(
    "pending_review", "approved", "rejected", "paid",
    name="document_status",
    create_type=False,
)


def upgrade() -> None:
    document_type_enum.create(op.get_bind(), checkfirst=True)
    document_status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "documents",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("file_path", sa.String(1024), nullable=False),
        sa.Column("file_hash", sa.String(64), nullable=False, unique=True),
        sa.Column("original_filename", sa.String(512)),
        sa.Column("doc_type", document_type_enum, nullable=False, server_default="unknown"),
        sa.Column("status", document_status_enum, nullable=False, server_default="pending_review"),
        sa.Column("doc_date", sa.Date),
        sa.Column("due_date", sa.Date),
        sa.Column("vendor", sa.String(255)),
        sa.Column("category", sa.String(128)),
        sa.Column("currency", sa.String(3), nullable=False, server_default="EUR"),
        sa.Column("amount_gross", sa.Numeric(14, 2)),
        sa.Column("amount_tax", sa.Numeric(14, 2)),
        sa.Column("assigned_to", sa.String(255)),
        sa.Column("decided_at", sa.DateTime(timezone=True)),
        sa.Column("decided_by", sa.String(255)),
        sa.Column("decision_note", sa.String(1024)),
        sa.Column("raw_json", postgresql.JSONB),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_documents_doc_date", "documents", ["doc_date"])
    op.create_index("ix_documents_vendor", "documents", ["vendor"])
    op.create_index("ix_documents_status", "documents", ["status"])
    op.create_index("ix_documents_doc_type", "documents", ["doc_type"])

    op.create_table(
        "audit_log",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "document_id",
            sa.Integer,
            sa.ForeignKey("documents.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("actor", sa.String(255), nullable=False),
        sa.Column("action", sa.String(64), nullable=False),
        sa.Column("from_status", sa.String(64)),
        sa.Column("to_status", sa.String(64)),
        sa.Column("note", sa.String(1024)),
        sa.Column("extra", postgresql.JSONB),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_audit_log_document_id", "audit_log", ["document_id"])
    op.create_index("ix_audit_log_created_at", "audit_log", ["created_at"])

    op.create_table(
        "approval_rules",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("priority", sa.Integer, nullable=False, server_default="100"),
        sa.Column("doc_type", sa.String(32)),
        sa.Column("category", sa.String(128)),
        sa.Column("vendor_pattern", sa.String(255)),
        sa.Column("amount_min", sa.Numeric(14, 2)),
        sa.Column("amount_max", sa.Numeric(14, 2)),
        sa.Column("approver_email", sa.String(255), nullable=False),
        sa.Column("active", sa.Boolean, nullable=False, server_default=sa.true()),
    )


def downgrade() -> None:
    op.drop_table("approval_rules")
    op.drop_index("ix_audit_log_created_at", table_name="audit_log")
    op.drop_index("ix_audit_log_document_id", table_name="audit_log")
    op.drop_table("audit_log")
    op.drop_index("ix_documents_doc_type", table_name="documents")
    op.drop_index("ix_documents_status", table_name="documents")
    op.drop_index("ix_documents_vendor", table_name="documents")
    op.drop_index("ix_documents_doc_date", table_name="documents")
    op.drop_table("documents")
    document_status_enum.drop(op.get_bind(), checkfirst=True)
    document_type_enum.drop(op.get_bind(), checkfirst=True)
