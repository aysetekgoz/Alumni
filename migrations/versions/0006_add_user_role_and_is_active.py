"""add role and is_active to users, make graduation_year nullable

Revision ID: 0006
Revises: 0005
Create Date: 2026-11-25
"""
from alembic import op
import sqlalchemy as sa

revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("role", sa.String(20), nullable=False, server_default="alumni"),
    )
    op.add_column(
        "users",
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.alter_column(
        "users",
        "graduation_year",
        existing_type=sa.Integer(),
        nullable=True,
    )
    op.create_check_constraint(
        "ck_users_role",
        "users",
        "role IN ('admin','staff','academic','student','alumni')",
    )
    op.create_index("ix_users_role", "users", ["role"])


def downgrade() -> None:
    op.drop_index("ix_users_role", table_name="users")
    op.drop_constraint("ck_users_role", "users", type_="check")
    op.execute("UPDATE users SET graduation_year = 2026 WHERE graduation_year IS NULL")
    op.alter_column(
        "users",
        "graduation_year",
        existing_type=sa.Integer(),
        nullable=False,
    )
    op.drop_column("users", "is_active")
    op.drop_column("users", "role")
