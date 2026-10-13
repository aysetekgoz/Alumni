import os
from typing import Any, Dict, List

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)  # .html şablonlarda otomatik HTML-escape (XSS koruması)


class AnnouncementView:
    """View katmanı: duyuru sayfalarını Jinja2 şablonlarıyla üretir."""

    @staticmethod
    def render_list(request: Request, announcements: List[Dict[str, Any]]) -> HTMLResponse:
        return templates.TemplateResponse(request, "announcements.html", {"announcements": announcements})

    @staticmethod
    def render_detail(request: Request, announcement: Dict[str, Any]) -> HTMLResponse:
        return templates.TemplateResponse(request, "announcement_detail.html", {"announcement": announcement})

    @staticmethod
    def render_edit(request: Request, announcement: Dict[str, Any]) -> HTMLResponse:
        return templates.TemplateResponse(request, "announcement_edit.html", {"announcement": announcement})
