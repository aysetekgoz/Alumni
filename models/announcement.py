from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel
from sqlalchemy import text

from database.session import session_scope
from database.tables import AnnouncementTable


class AnnouncementCreate(BaseModel):
    """Schema for creating an announcement (id and created_at are auto-assigned)."""
    title: str
    content: str
    author: str


class AnnouncementUpdate(BaseModel):
    """Schema for full update (PUT)."""
    title: str
    content: str
    author: str


class AnnouncementPatch(BaseModel):
    """Schema for partial update (PATCH)."""
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None


_FIELDS = ("title", "content", "author")


def _row_to_dict(row: AnnouncementTable) -> Dict[str, Any]:
    created = row.created_at
    return {
        "id": row.id,
        "title": row.title,
        "content": row.content,
        "author": row.author,
        "created_at": created.isoformat(timespec="seconds") if isinstance(created, datetime) else created,
    }


class Announcement:
    """
    Announcement model backed by PostgreSQL (SQLAlchemy). Table: announcements (see ddd.md).
    All CRUD functions live here; they return None when the id does not exist
    (controllers turn that into HTTP 404).
    """

    @staticmethod
    def _to_payload(data: Union[Dict[str, Any], BaseModel], partial: bool = False) -> Dict[str, Any]:
        if hasattr(data, "model_dump"):
            return data.model_dump(exclude_unset=True) if partial else data.model_dump()
        if isinstance(data, dict):
            return {k: v for k, v in data.items() if not partial or v is not None}
        raise ValueError("Unsupported data format")

    @classmethod
    def create(cls, data: Union[Dict[str, Any], AnnouncementCreate]) -> Dict[str, Any]:
        payload = cls._to_payload(data)
        with session_scope() as session:
            row = AnnouncementTable(
                title=payload.get("title"),
                content=payload.get("content"),
                author=payload.get("author"),
            )
            session.add(row)
            session.flush()
            session.refresh(row)  # created_at (server_default) değerini al
            return _row_to_dict(row)

    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        with session_scope() as session:
            rows = session.query(AnnouncementTable).order_by(AnnouncementTable.id).all()
            return [_row_to_dict(r) for r in rows]

    @classmethod
    def get_by_id(cls, announcement_id: int) -> Optional[Dict[str, Any]]:
        with session_scope() as session:
            row = session.get(AnnouncementTable, announcement_id)
            return _row_to_dict(row) if row else None

    @classmethod
    def update(cls, announcement_id: int, data: Union[Dict[str, Any], AnnouncementUpdate]) -> Optional[Dict[str, Any]]:
        payload = cls._to_payload(data)
        with session_scope() as session:
            row = session.get(AnnouncementTable, announcement_id)
            if row is None:
                return None
            for key in _FIELDS:
                if key in payload:
                    setattr(row, key, payload[key])
            session.flush()
            return _row_to_dict(row)

    @classmethod
    def patch(cls, announcement_id: int, data: Union[Dict[str, Any], AnnouncementPatch]) -> Optional[Dict[str, Any]]:
        payload = cls._to_payload(data, partial=True)
        with session_scope() as session:
            row = session.get(AnnouncementTable, announcement_id)
            if row is None:
                return None
            for key in _FIELDS:
                if key in payload and payload[key] is not None:
                    setattr(row, key, payload[key])
            session.flush()
            return _row_to_dict(row)

    @classmethod
    def delete(cls, announcement_id: int) -> Optional[Dict[str, Any]]:
        with session_scope() as session:
            row = session.get(AnnouncementTable, announcement_id)
            if row is None:
                return None
            deleted = _row_to_dict(row)
            session.delete(row)
            return deleted

    @classmethod
    def clear(cls) -> None:
        with session_scope() as session:
            session.execute(text("TRUNCATE TABLE announcements RESTART IDENTITY"))
