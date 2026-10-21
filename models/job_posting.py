from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel
from sqlalchemy import text

from database.session import session_scope
from database.tables import JobPostingTable

EmploymentType = Literal["full_time", "part_time", "internship", "contract"]


class JobPostingCreate(BaseModel):
    """Schema for creating a job posting (id and created_at are auto-assigned)."""
    title: str
    company: str
    location: str
    description: str
    employment_type: EmploymentType = "full_time"
    is_active: bool = True
    posted_by: Optional[int] = None  # users.id (FK), optional


class JobPostingUpdate(BaseModel):
    """Schema for full update (PUT)."""
    title: str
    company: str
    location: str
    description: str
    employment_type: EmploymentType
    is_active: bool
    posted_by: Optional[int] = None


class JobPostingPatch(BaseModel):
    """Schema for partial update (PATCH)."""
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    employment_type: Optional[EmploymentType] = None
    is_active: Optional[bool] = None
    posted_by: Optional[int] = None


_FIELDS = (
    "title", "company", "location", "description",
    "employment_type", "is_active", "posted_by",
)


def _row_to_dict(row: JobPostingTable) -> Dict[str, Any]:
    created = row.created_at
    return {
        "id": row.id,
        "title": row.title,
        "company": row.company,
        "location": row.location,
        "employment_type": row.employment_type,
        "description": row.description,
        "is_active": row.is_active,
        "posted_by": row.posted_by,
        "created_at": created.isoformat(timespec="seconds") if isinstance(created, datetime) else created,
    }


class JobPosting:
    """
    JobPosting model backed by PostgreSQL (SQLAlchemy). Table: job_postings (see ddd.md).
    Relationship: users (1) -> job_postings (N) via posted_by (ON DELETE SET NULL).
    Functions return None when the id does not exist (controllers turn that into 404).
    """

    @staticmethod
    def _to_payload(data: Union[Dict[str, Any], BaseModel], partial: bool = False) -> Dict[str, Any]:
        if hasattr(data, "model_dump"):
            return data.model_dump(exclude_unset=True) if partial else data.model_dump()
        if isinstance(data, dict):
            return {k: v for k, v in data.items() if not partial or v is not None}
        raise ValueError("Unsupported data format")

    @classmethod
    def create(cls, data: Union[Dict[str, Any], JobPostingCreate]) -> Dict[str, Any]:
        payload = cls._to_payload(data)
        with session_scope() as session:
            row = JobPostingTable(**{k: payload[k] for k in _FIELDS if k in payload})
            session.add(row)
            session.flush()
            session.refresh(row)
            return _row_to_dict(row)

    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        with session_scope() as session:
            rows = session.query(JobPostingTable).order_by(JobPostingTable.id).all()
            return [_row_to_dict(r) for r in rows]

    @classmethod
    def get_by_id(cls, job_id: int) -> Optional[Dict[str, Any]]:
        with session_scope() as session:
            row = session.get(JobPostingTable, job_id)
            return _row_to_dict(row) if row else None

    @classmethod
    def get_by_user(cls, user_id: int) -> List[Dict[str, Any]]:
        """All postings created by a given user (relationship users -> job_postings)."""
        with session_scope() as session:
            rows = (
                session.query(JobPostingTable)
                .filter(JobPostingTable.posted_by == user_id)
                .order_by(JobPostingTable.id)
                .all()
            )
            return [_row_to_dict(r) for r in rows]

    @classmethod
    def update(cls, job_id: int, data: Union[Dict[str, Any], JobPostingUpdate]) -> Optional[Dict[str, Any]]:
        payload = cls._to_payload(data)
        with session_scope() as session:
            row = session.get(JobPostingTable, job_id)
            if row is None:
                return None
            for key in _FIELDS:
                if key in payload:
                    setattr(row, key, payload[key])
            session.flush()
            return _row_to_dict(row)

    @classmethod
    def patch(cls, job_id: int, data: Union[Dict[str, Any], JobPostingPatch]) -> Optional[Dict[str, Any]]:
        payload = cls._to_payload(data, partial=True)
        with session_scope() as session:
            row = session.get(JobPostingTable, job_id)
            if row is None:
                return None
            for key in _FIELDS:
                if key in payload and payload[key] is not None:
                    setattr(row, key, payload[key])
            session.flush()
            return _row_to_dict(row)

    @classmethod
    def delete(cls, job_id: int) -> Optional[Dict[str, Any]]:
        with session_scope() as session:
            row = session.get(JobPostingTable, job_id)
            if row is None:
                return None
            deleted = _row_to_dict(row)
            session.delete(row)
            return deleted

    @classmethod
    def clear(cls) -> None:
        with session_scope() as session:
            session.execute(text("TRUNCATE TABLE job_postings RESTART IDENTITY"))
