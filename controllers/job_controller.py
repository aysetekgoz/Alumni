from typing import Any, Dict, Optional

from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from models.application import Application
from models.job_posting import JobPosting
from models.user import User
from views.job_view import JobView

router = APIRouter(tags=["Job"])

NOT_FOUND = "İş ilanı bulunamadı"
EMPLOYMENT_TYPES = ("full_time", "part_time", "internship", "contract")
APPLICATION_STATUSES = ("pending", "reviewed", "accepted", "rejected")


class JobController:
    """HTML controller: iş ilanları ve başvurular için temel arayüzler."""

    @classmethod
    def get_or_404(cls, job_id: int) -> Dict[str, Any]:
        job = JobPosting.get_by_id(job_id)
        if job is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
        return job

    @classmethod
    def index(cls, request: Request) -> HTMLResponse:
        return JobView.render_list(request, JobPosting.get_all(), User.get_all())

    @classmethod
    def show(cls, request: Request, job_id: int) -> HTMLResponse:
        job = cls.get_or_404(job_id)
        applications = Application.get_by_job_posting(job_id)
        return JobView.render_detail(request, job, applications, User.get_all())

    @classmethod
    def create(
        cls, title: str, company: str, location: str, description: str,
        employment_type: str, posted_by: Optional[str],
    ) -> RedirectResponse:
        if employment_type not in EMPLOYMENT_TYPES:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Geçersiz çalışma türü")
        JobPosting.create({
            "title": title, "company": company, "location": location, "description": description,
            "employment_type": employment_type,
            "posted_by": int(posted_by) if posted_by else None,
        })
        return RedirectResponse("/jobs", status_code=status.HTTP_303_SEE_OTHER)

    @classmethod
    def apply(cls, job_id: int, user_id: int, cover_letter: Optional[str]) -> RedirectResponse:
        cls.get_or_404(job_id)
        if User.get_by_id(user_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kullanıcı bulunamadı")
        Application.create({
            "job_posting_id": job_id, "user_id": user_id,
            "cover_letter": cover_letter or None, "status": "pending",
        })
        return RedirectResponse(f"/jobs/{job_id}", status_code=status.HTTP_303_SEE_OTHER)

    @classmethod
    def applications(cls, request: Request) -> HTMLResponse:
        jobs = {j["id"]: j for j in JobPosting.get_all()}
        users = {u["id"]: u for u in User.get_all()}
        return JobView.render_applications(request, Application.get_all(), jobs, users)


@router.get("/jobs", summary="İş ilanları listesi + ilan ekleme formu", response_class=HTMLResponse)
def list_jobs(request: Request):
    return JobController.index(request)


@router.post("/jobs", summary="İş ilanı oluştur", status_code=status.HTTP_303_SEE_OTHER)
def create_job(
    title: str = Form(...),
    company: str = Form(...),
    location: str = Form(...),
    description: str = Form(...),
    employment_type: str = Form("full_time"),
    posted_by: Optional[str] = Form(None),
):
    return JobController.create(title, company, location, description, employment_type, posted_by)


@router.get("/jobs/{job_id}", summary="İlan detayı + başvuru formu", response_class=HTMLResponse)
def show_job(request: Request, job_id: int):
    return JobController.show(request, job_id)


@router.post("/jobs/{job_id}/apply", summary="İlana başvur", status_code=status.HTTP_303_SEE_OTHER)
def apply_job(job_id: int, user_id: int = Form(...), cover_letter: Optional[str] = Form(None)):
    return JobController.apply(job_id, user_id, cover_letter)


@router.get("/applications", summary="Başvurular listesi + başvuru formu", response_class=HTMLResponse)
def list_applications(request: Request):
    return JobController.applications(request)


@router.post("/applications", summary="Başvuru oluştur", status_code=status.HTTP_303_SEE_OTHER)
def create_application(
    job_posting_id: int = Form(...),
    user_id: int = Form(...),
    cover_letter: Optional[str] = Form(None),
):
    JobController.apply(job_posting_id, user_id, cover_letter)
    return RedirectResponse("/applications", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/applications/{application_id}/status", summary="Başvuru durumunu güncelle",
             status_code=status.HTTP_303_SEE_OTHER)
def update_application_status(application_id: int, new_status: str = Form(..., alias="status")):
    if new_status not in APPLICATION_STATUSES:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Geçersiz durum")
    if Application.patch(application_id, {"status": new_status}) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Başvuru bulunamadı")
    return RedirectResponse("/applications", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/applications/{application_id}/delete", summary="Başvuruyu sil",
             status_code=status.HTTP_303_SEE_OTHER)
def delete_application(application_id: int):
    if Application.delete(application_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Başvuru bulunamadı")
    return RedirectResponse("/applications", status_code=status.HTTP_303_SEE_OTHER)

