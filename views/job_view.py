from typing import Any, Dict, List

from fastapi import Request
from fastapi.responses import HTMLResponse

from views.announcement_view import templates


class JobView:
    """View katmanı: iş ilanı ve başvuru sayfalarını Jinja2 şablonlarıyla üretir."""

    @staticmethod
    def render_list(request: Request, jobs: List[Dict[str, Any]], users: List[Dict[str, Any]]) -> HTMLResponse:
        return templates.TemplateResponse(request, "jobs.html", {"jobs": jobs, "users": users})

    @staticmethod
    def render_detail(
        request: Request, job: Dict[str, Any], applications: List[Dict[str, Any]], users: List[Dict[str, Any]]
    ) -> HTMLResponse:
        return templates.TemplateResponse(
            request, "job_detail.html", {"job": job, "applications": applications, "users": users}
        )

    @staticmethod
    def render_applications(
        request: Request,
        applications: List[Dict[str, Any]],
        jobs: Dict[int, Dict[str, Any]],
        users: Dict[int, Dict[str, Any]],
    ) -> HTMLResponse:
        return templates.TemplateResponse(
            request, "applications.html", {"applications": applications, "jobs": jobs, "users": users}
        )

