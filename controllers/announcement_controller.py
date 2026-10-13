from typing import Any, Dict

from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from models.announcement import Announcement
from views.announcement_view import AnnouncementView

router = APIRouter(prefix="/announcements", tags=["Announcement"])

NOT_FOUND = "Duyuru bulunamadı"


class AnnouncementController:
    """HTML controller. Independent from ApiAnnouncementController (no inheritance).
    Sunum için AnnouncementView (Jinja2, otomatik HTML-escape) kullanılır."""

    @classmethod
    def get_or_404(cls, announcement_id: int) -> Dict[str, Any]:
        item = Announcement.get_by_id(announcement_id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
        return item

    @classmethod
    def index(cls, request: Request) -> HTMLResponse:
        return AnnouncementView.render_list(request, Announcement.get_all())

    @classmethod
    def show(cls, request: Request, announcement_id: int) -> HTMLResponse:
        return AnnouncementView.render_detail(request, cls.get_or_404(announcement_id))

    @classmethod
    def edit_form(cls, request: Request, announcement_id: int) -> HTMLResponse:
        return AnnouncementView.render_edit(request, cls.get_or_404(announcement_id))

    @classmethod
    def create(cls, title: str, content: str, author: str) -> RedirectResponse:
        Announcement.create({"title": title, "content": content, "author": author})
        return RedirectResponse("/announcements", status_code=status.HTTP_303_SEE_OTHER)

    @classmethod
    def update(cls, announcement_id: int, title: str, content: str, author: str) -> RedirectResponse:
        cls.get_or_404(announcement_id)
        Announcement.update(announcement_id, {"title": title, "content": content, "author": author})
        return RedirectResponse(f"/announcements/{announcement_id}", status_code=status.HTTP_303_SEE_OTHER)

    @classmethod
    def delete(cls, announcement_id: int) -> RedirectResponse:
        cls.get_or_404(announcement_id)
        Announcement.delete(announcement_id)
        return RedirectResponse("/announcements", status_code=status.HTTP_303_SEE_OTHER)


@router.get("", summary="Duyuru listesi + ekleme formu", response_class=HTMLResponse)
def list_announcements(request: Request):
    return AnnouncementController.index(request)


@router.post("", summary="Duyuru oluştur", status_code=status.HTTP_303_SEE_OTHER)
def create_announcement(title: str = Form(...), content: str = Form(...), author: str = Form(...)):
    return AnnouncementController.create(title, content, author)


@router.get("/{announcement_id}", summary="Duyuru detayı", response_class=HTMLResponse)
def show_announcement(request: Request, announcement_id: int):
    return AnnouncementController.show(request, announcement_id)


@router.get("/{announcement_id}/edit", summary="Düzenleme formu", response_class=HTMLResponse)
def edit_announcement_form(request: Request, announcement_id: int):
    return AnnouncementController.edit_form(request, announcement_id)


@router.post("/{announcement_id}/edit", summary="Duyuruyu güncelle", status_code=status.HTTP_303_SEE_OTHER)
def update_announcement(
    announcement_id: int,
    title: str = Form(...),
    content: str = Form(...),
    author: str = Form(...),
):
    return AnnouncementController.update(announcement_id, title, content, author)


@router.post("/{announcement_id}/delete", summary="Duyuruyu sil", status_code=status.HTTP_303_SEE_OTHER)
def delete_announcement(announcement_id: int):
    return AnnouncementController.delete(announcement_id)
