"""create applications table (ddd.md section 3.4)

Revision ID: 0003
Revises: 0002
Create Date: 2026-10-21
"""
from alembic import op
import sqlalchemy as sa

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "applications",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "job_posting_id",
            sa.Integer(),
            sa.ForeignKey(
                "job_postings.id", ondelete="CASCADE", name="fk_applications_job_posting_id"
            ),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE", name="fk_applications_user_id"),
            nullable=False,
        ),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("cover_letter", sa.Text(), nullable=True),
        sa.Column(
            "applied_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.CheckConstraint(
            "status IN ('pending','reviewed','accepted','rejected')",
            name="ck_applications_status",
        ),
        sa.UniqueConstraint(
            "job_posting_id", "user_id", name="uq_applications_job_user"
        ),
    )
    op.create_index("ix_applications_user_id", "applications", ["user_id"])
    op.create_index("ix_applications_status", "applications", ["status"])


def downgrade() -> None:
    op.drop_index("ix_applications_status", table_name="applications")
    op.drop_index("ix_applications_user_id", table_name="applications")
    op.drop_table("applications")
