"""
SQLAlchemy table definitions. Source of truth: ddd.md (Data Design Documentation).
These are schema definitions used by Alembic migrations; the CRUD model layer
(models/) is still in-memory and is not changed here.
"""
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
    true,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    graduation_year = Column(Integer, nullable=False)
    department = Column(String(150), nullable=False)

    job_postings = relationship("JobPostingTable", back_populates="poster")
    applications = relationship(
        "ApplicationTable",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

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


class JobPostingTable(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    company = Column(String(150), nullable=False)
    location = Column(String(150), nullable=False)
    employment_type = Column(
        String(30), nullable=False, server_default="full_time"
    )
    description = Column(Text, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default=true())
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    posted_by = Column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    poster = relationship("UserTable", back_populates="job_postings")
    applications = relationship(
        "ApplicationTable",
        back_populates="job_posting",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    __table_args__ = (
        CheckConstraint(
            "employment_type IN ('full_time','part_time','internship','contract')",
            name="ck_job_postings_employment_type",
        ),
        Index("ix_job_postings_created_at", created_at.desc()),
        Index("ix_job_postings_company", "company"),
        Index("ix_job_postings_is_active", "is_active"),
        Index("ix_job_postings_posted_by", "posted_by"),
    )


class ApplicationTable(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_posting_id = Column(
        Integer, ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    status = Column(String(20), nullable=False, server_default="pending")
    cover_letter = Column(Text, nullable=True)
    applied_at = Column(DateTime, nullable=False, server_default=func.now())

    user = relationship("UserTable", back_populates="applications")
    job_posting = relationship("JobPostingTable", back_populates="applications")

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending','reviewed','accepted','rejected')",
            name="ck_applications_status",
        ),
        UniqueConstraint("job_posting_id", "user_id", name="uq_applications_job_user"),
        Index("ix_applications_user_id", "user_id"),
        Index("ix_applications_status", "status"),
    )
