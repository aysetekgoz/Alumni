"""initial schema: users and announcements (ddd.md)

Revision ID: 0001
Revises:
Create Date: 2026-10-14
"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("graduation_year", sa.Integer(), nullable=False),
        sa.Column("department", sa.String(150), nullable=False),
        sa.CheckConstraint(
            "graduation_year BETWEEN 1900 AND 2100", name="ck_users_graduation_year"
        ),
        sa.CheckConstraint("email = lower(email)", name="ck_users_email_lowercase"),
    )
    op.create_index("uq_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_department", "users", ["department"])
    op.create_index("ix_users_graduation_year", "users", ["graduation_year"])

    op.create_table(
        "announcements",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("author", sa.String(150), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_index(
        "ix_announcements_created_at", "announcements", [sa.text("created_at DESC")]
    )


def downgrade() -> None:
    op.drop_index("ix_announcements_created_at", table_name="announcements")
    op.drop_table("announcements")
    op.drop_index("ix_users_graduation_year", table_name="users")
    op.drop_index("ix_users_department", table_name="users")
    op.drop_index("uq_users_email", table_name="users")
    op.drop_table("users")
