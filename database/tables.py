"""
SQLAlchemy table definitions. Source of truth: ddd.md (Data Design Documentation).
These are schema definitions used by Alembic migrations; the CRUD model layer
(models/) is still in-memory and is not changed here.
"""
from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    graduation_year = Column(Integer, nullable=False)
    department = Column(String(150), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "graduation_year BETWEEN 1900 AND 2100", name="ck_users_graduation_year"
        ),
        CheckConstraint("email = lower(email)", name="ck_users_email_lowercase"),
        Index("uq_users_email", "email", unique=True),
        Index("ix_users_department", "department"),
        Index("ix_users_graduation_year", "graduation_year"),
    )


class AnnouncementTable(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(150), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    __table_args__ = (
        Index("ix_announcements_created_at", created_at.desc()),
    )
