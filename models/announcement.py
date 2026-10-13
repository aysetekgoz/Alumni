from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


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


class Announcement:
    """
    Announcement model without database. Data is kept in an in-memory list.
    All CRUD functions live here; they return None when the id does not exist
    (controllers turn that into HTTP 404).
    """

    _db: List[Dict[str, Any]] = []
    _auto_increment_id: int = 1

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
        item = {
            "id": cls._auto_increment_id,
            "title": payload.get("title"),
            "content": payload.get("content"),
            "author": payload.get("author"),
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
        cls._auto_increment_id += 1
        cls._db.append(item)
        return item

    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        return cls._db

    @classmethod
    def get_by_id(cls, announcement_id: int) -> Optional[Dict[str, Any]]:
        for item in cls._db:
            if item["id"] == announcement_id:
                return item
        return None

    @classmethod
    def update(cls, announcement_id: int, data: Union[Dict[str, Any], AnnouncementUpdate]) -> Optional[Dict[str, Any]]:
        item = cls.get_by_id(announcement_id)
        if item is None:
            return None
        payload = cls._to_payload(data)
        for key in ("title", "content", "author"):
            if key in payload:
                item[key] = payload[key]
        return item

    @classmethod
    def patch(cls, announcement_id: int, data: Union[Dict[str, Any], AnnouncementPatch]) -> Optional[Dict[str, Any]]:
        item = cls.get_by_id(announcement_id)
        if item is None:
            return None
        payload = cls._to_payload(data, partial=True)
        for key in ("title", "content", "author"):
            if key in payload and payload[key] is not None:
                item[key] = payload[key]
        return item

    @classmethod
    def delete(cls, announcement_id: int) -> Optional[Dict[str, Any]]:
        for index, item in enumerate(cls._db):
            if item["id"] == announcement_id:
                return cls._db.pop(index)
        return None

    @classmethod
    def clear(cls) -> None:
        cls._db.clear()
        cls._auto_increment_id = 1
