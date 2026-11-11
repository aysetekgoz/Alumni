"""update job_postings rules (title max 120, city & description optional, add application_url)

Revision ID: 0004
Revises: 0003
Create Date: 2026-11-11
"""
from alembic import op
import sqlalchemy as sa

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "job_postings",
        "title",
        existing_type=sa.String(200),
        type_=sa.String(120),
        existing_nullable=False,
    )
    op.alter_column(
        "job_postings",
        "location",
        new_column_name="city",
        existing_type=sa.String(150),
        nullable=True,
    )
    op.alter_column(
        "job_postings",
        "description",
        existing_type=sa.Text(),
        nullable=True,
    )
    op.add_column(
        "job_postings",
        sa.Column("application_url", sa.String(500), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("job_postings", "application_url")
    op.execute("UPDATE job_postings SET description = '' WHERE description IS NULL")
    op.alter_column(
        "job_postings",
        "description",
        existing_type=sa.Text(),
        nullable=False,
    )
    op.execute("UPDATE job_postings SET city = '' WHERE city IS NULL")
    op.alter_column(
        "job_postings",
        "city",
        new_column_name="location",
        existing_type=sa.String(150),
        nullable=False,
    )
    op.alter_column(
        "job_postings",
        "title",
        existing_type=sa.String(120),
        type_=sa.String(200),
        existing_nullable=False,
    )
