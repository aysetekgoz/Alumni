from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, status

from models.announcement import (
    Announcement,
    AnnouncementCreate,
    AnnouncementPatch,
    AnnouncementUpdate,
)

router = APIRouter(prefix="/api/announcements", tags=["ApiAnnouncement"])

NOT_FOUND = "Duyuru bulunamadı"


class ApiAnnouncementController:
    """JSON REST controller. Independent from AnnouncementController (no inheritance)."""

    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        return Announcement.get_all()

    @classmethod
    def get_by_id(cls, announcement_id: int) -> Dict[str, Any]:
        item = Announcement.get_by_id(announcement_id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
        return item

    @classmethod
    def create(cls, data: AnnouncementCreate) -> Dict[str, Any]:
        return Announcement.create(data)

    @classmethod
    def update(cls, announcement_id: int, data: AnnouncementUpdate) -> Dict[str, Any]:
        item = Announcement.update(announcement_id, data)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
        return item

    @classmethod
    def patch(cls, announcement_id: int, data: AnnouncementPatch) -> Dict[str, Any]:
        item = Announcement.patch(announcement_id, data)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
        return item

    @classmethod
    def delete(cls, announcement_id: int) -> Dict[str, Any]:
        item = Announcement.delete(announcement_id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
        return {"message": "Duyuru silindi", "announcement": item}


@router.get("", summary="Tüm duyuruları listele")
def api_list_announcements():
    return ApiAnnouncementController.get_all()


@router.post("", summary="Duyuru oluştur", status_code=status.HTTP_201_CREATED)
def api_create_announcement(data: AnnouncementCreate):
    return ApiAnnouncementController.create(data)


@router.get("/{announcement_id}", summary="Duyuru detayı")
def api_get_announcement(announcement_id: int):
    return ApiAnnouncementController.get_by_id(announcement_id)


@router.put("/{announcement_id}", summary="Duyuruyu tamamen güncelle")
def api_update_announcement(announcement_id: int, data: AnnouncementUpdate):
    return ApiAnnouncementController.update(announcement_id, data)


@router.patch("/{announcement_id}", summary="Duyuruyu kısmen güncelle")
def api_patch_announcement(announcement_id: int, data: AnnouncementPatch):
    return ApiAnnouncementController.patch(announcement_id, data)


@router.delete("/{announcement_id}", summary="Duyuruyu sil")
def api_delete_announcement(announcement_id: int):
    return ApiAnnouncementController.delete(announcement_id)
