from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel
from sqlalchemy import text

from database.session import session_scope
from database.tables import ApplicationTable

ApplicationStatus = Literal["pending", "reviewed", "accepted", "rejected"]


class ApplicationCreate(BaseModel):
    """Schema for creating an application (id and applied_at are auto-assigned)."""
    job_posting_id: int  # job_postings.id (FK)
    user_id: int  # users.id (FK)
    cover_letter: Optional[str] = None
    status: ApplicationStatus = "pending"


class ApplicationUpdate(BaseModel):
    """Schema for full update (PUT). job_posting_id, user_id and applied_at do not change."""
    status: ApplicationStatus
    cover_letter: Optional[str] = None


class ApplicationPatch(BaseModel):
    """Schema for partial update (PATCH)."""
    status: Optional[ApplicationStatus] = None
    cover_letter: Optional[str] = None


_CREATE_FIELDS = ("job_posting_id", "user_id", "cover_letter", "status")
_UPDATE_FIELDS = ("status", "cover_letter")


def _row_to_dict(row: ApplicationTable) -> Dict[str, Any]:
    applied = row.applied_at
    return {
        "id": row.id,
        "job_posting_id": row.job_posting_id,
        "user_id": row.user_id,
        "status": row.status,
        "cover_letter": row.cover_letter,
        "applied_at": applied.isoformat(timespec="seconds") if isinstance(applied, datetime) else applied,
    }


class Application:
    """
    Application model backed by PostgreSQL (SQLAlchemy). Table: applications (see ddd.md).
    Relationships: users (1) -> applications (N) and job_postings (1) -> applications (N).
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
    def create(cls, data: Union[Dict[str, Any], ApplicationCreate]) -> Dict[str, Any]:
        payload = cls._to_payload(data)
        with session_scope() as session:
            row = ApplicationTable(**{k: payload[k] for k in _CREATE_FIELDS if k in payload})
            session.add(row)
            session.flush()
            session.refresh(row)  # applied_at (server_default) değerini al
            return _row_to_dict(row)

    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        with session_scope() as session:
            rows = session.query(ApplicationTable).order_by(ApplicationTable.id).all()
            return [_row_to_dict(r) for r in rows]

    @classmethod
    def get_by_id(cls, application_id: int) -> Optional[Dict[str, Any]]:
        with session_scope() as session:
            row = session.get(ApplicationTable, application_id)
            return _row_to_dict(row) if row else None

    @classmethod
    def get_by_user(cls, user_id: int) -> List[Dict[str, Any]]:
        """All applications made by a given user (users -> applications)."""
        with session_scope() as session:
            rows = (
                session.query(ApplicationTable)
                .filter(ApplicationTable.user_id == user_id)
                .order_by(ApplicationTable.id)
                .all()
            )
            return [_row_to_dict(r) for r in rows]

    @classmethod
    def get_by_job_posting(cls, job_posting_id: int) -> List[Dict[str, Any]]:
        """All applications received by a given job posting (job_postings -> applications)."""
        with session_scope() as session:
            rows = (
                session.query(ApplicationTable)
                .filter(ApplicationTable.job_posting_id == job_posting_id)
                .order_by(ApplicationTable.id)
                .all()
            )
            return [_row_to_dict(r) for r in rows]

    @classmethod
    def update(cls, application_id: int, data: Union[Dict[str, Any], ApplicationUpdate]) -> Optional[Dict[str, Any]]:
        payload = cls._to_payload(data)
        with session_scope() as session:
            row = session.get(ApplicationTable, application_id)
            if row is None:
                return None
            for key in _UPDATE_FIELDS:
                if key in payload:
                    setattr(row, key, payload[key])
            session.flush()
            return _row_to_dict(row)

    @classmethod
    def patch(cls, application_id: int, data: Union[Dict[str, Any], ApplicationPatch]) -> Optional[Dict[str, Any]]:
        payload = cls._to_payload(data, partial=True)
        with session_scope() as session:
            row = session.get(ApplicationTable, application_id)
            if row is None:
                return None
            for key in _UPDATE_FIELDS:
                if key in payload and payload[key] is not None:
                    setattr(row, key, payload[key])
            session.flush()
            return _row_to_dict(row)

    @classmethod
    def delete(cls, application_id: int) -> Optional[Dict[str, Any]]:
        with session_scope() as session:
            row = session.get(ApplicationTable, application_id)
            if row is None:
                return None
            deleted = _row_to_dict(row)
            session.delete(row)
            return deleted

    @classmethod
    def clear(cls) -> None:
        with session_scope() as session:
            session.execute(text("TRUNCATE TABLE applications RESTART IDENTITY"))
