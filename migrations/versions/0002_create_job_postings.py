"""create job_postings table (ddd.md section 3.3)

Revision ID: 0002
Revises: 0001
Create Date: 2026-10-21
"""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "job_postings",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("company", sa.String(150), nullable=False),
        sa.Column("location", sa.String(150), nullable=False),
        sa.Column(
            "employment_type",
            sa.String(30),
            nullable=False,
            server_default="full_time",
        ),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column(
            "is_active", sa.Boolean(), nullable=False, server_default=sa.true()
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "posted_by",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="SET NULL", name="fk_job_postings_posted_by"),
            nullable=True,
        ),
        sa.CheckConstraint(
            "employment_type IN ('full_time','part_time','internship','contract')",
            name="ck_job_postings_employment_type",
        ),
    )
    op.create_index(
        "ix_job_postings_created_at", "job_postings", [sa.text("created_at DESC")]
    )
    op.create_index("ix_job_postings_company", "job_postings", ["company"])
    op.create_index("ix_job_postings_is_active", "job_postings", ["is_active"])
    op.create_index("ix_job_postings_posted_by", "job_postings", ["posted_by"])


def downgrade() -> None:
    op.drop_index("ix_job_postings_posted_by", table_name="job_postings")
    op.drop_index("ix_job_postings_is_active", table_name="job_postings")
    op.drop_index("ix_job_postings_company", table_name="job_postings")
    op.drop_index("ix_job_postings_created_at", table_name="job_postings")
    op.drop_table("job_postings")
