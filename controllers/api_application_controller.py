from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from models.application import (
    Application,
    ApplicationCreate,
    ApplicationPatch,
    ApplicationUpdate,
)
from models.job_posting import JobPosting
from models.user import User

# Direct routes: the resource is addressed on its own.            /api/applications
router = APIRouter(prefix="/api/applications", tags=["ApiApplication"])
# Nested routes: the resource is addressed through one of its parents.
#   /api/users/{user_id}/applications          (parent: user)
#   /api/job-postings/{job_id}/applications    (parent: job posting)
user_nested_router = APIRouter(
    prefix="/api/users/{user_id}/applications", tags=["ApiUserApplication"]
)
job_nested_router = APIRouter(
    prefix="/api/job-postings/{job_id}/applications", tags=["ApiJobPostingApplication"]
)

NOT_FOUND = "Başvuru bulunamadı"
USER_NOT_FOUND = "Kullanıcı bulunamadı"
JOB_NOT_FOUND = "İş ilanı bulunamadı"


class UserApplicationCreate(BaseModel):
    """Body for POST /api/users/{user_id}/applications (user_id comes from the URL)."""
    job_posting_id: int
    cover_letter: Optional[str] = None


class JobApplicationCreate(BaseModel):
    """Body for POST /api/job-postings/{job_id}/applications (job_posting_id comes from the URL)."""
    user_id: int
    cover_letter: Optional[str] = None


def _not_found(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ApiApplicationController:
    """JSON REST controller for applications (direct and nested routes)."""

    # ---- direct ----
    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        return Application.get_all()

    @classmethod
    def get_by_id(cls, application_id: int) -> Dict[str, Any]:
        item = Application.get_by_id(application_id)
        if item is None:
            raise _not_found(NOT_FOUND)
        return item

    @classmethod
    def create(cls, data: ApplicationCreate) -> Dict[str, Any]:
        # FK violations and duplicate (job, user) pairs are turned into an error
        # response by main.py's IntegrityError handler.
        return Application.create(data)

    @classmethod
    def update(cls, application_id: int, data: ApplicationUpdate) -> Dict[str, Any]:
        item = Application.update(application_id, data)
        if item is None:
            raise _not_found(NOT_FOUND)
        return item

    @classmethod
    def patch(cls, application_id: int, data: ApplicationPatch) -> Dict[str, Any]:
        item = Application.patch(application_id, data)
        if item is None:
            raise _not_found(NOT_FOUND)
        return item

    @classmethod
    def delete(cls, application_id: int) -> Dict[str, Any]:
        item = Application.delete(application_id)
        if item is None:
            raise _not_found(NOT_FOUND)
        return {"message": "Başvuru silindi", "application": item}

    # ---- nested (parent: user) ----
    @staticmethod
    def _require_user(user_id: int) -> None:
        if User.get_by_id(user_id) is None:
            raise _not_found(USER_NOT_FOUND)

    @classmethod
    def get_by_user(cls, user_id: int) -> List[Dict[str, Any]]:
        cls._require_user(user_id)
        return Application.get_by_user(user_id)

    @classmethod
    def get_user_application(cls, user_id: int, application_id: int) -> Dict[str, Any]:
        cls._require_user(user_id)
        item = Application.get_by_id(application_id)
        # An application that belongs to another user is not found under this user.
        if item is None or item["user_id"] != user_id:
            raise _not_found(NOT_FOUND)
        return item

    @classmethod
    def create_for_user(cls, user_id: int, data: UserApplicationCreate) -> Dict[str, Any]:
        cls._require_user(user_id)
        if JobPosting.get_by_id(data.job_posting_id) is None:
            raise _not_found(JOB_NOT_FOUND)
        payload = data.model_dump()
        payload["user_id"] = user_id  # taken from the URL
        return Application.create(payload)

    # ---- nested (parent: job posting) ----
    @staticmethod
    def _require_job(job_id: int) -> None:
        if JobPosting.get_by_id(job_id) is None:
            raise _not_found(JOB_NOT_FOUND)

    @classmethod
    def get_by_job(cls, job_id: int) -> List[Dict[str, Any]]:
        cls._require_job(job_id)
        return Application.get_by_job_posting(job_id)

    @classmethod
    def get_job_application(cls, job_id: int, application_id: int) -> Dict[str, Any]:
        cls._require_job(job_id)
        item = Application.get_by_id(application_id)
        if item is None or item["job_posting_id"] != job_id:
            raise _not_found(NOT_FOUND)
        return item

    @classmethod
    def create_for_job(cls, job_id: int, data: JobApplicationCreate) -> Dict[str, Any]:
        cls._require_job(job_id)
        if User.get_by_id(data.user_id) is None:
            raise _not_found(USER_NOT_FOUND)
        payload = data.model_dump()
        payload["job_posting_id"] = job_id  # taken from the URL
        return Application.create(payload)


# ---------------- Direct routes: /api/applications ----------------
@router.get("", summary="Tüm başvuruları listele")
def api_list_applications():
    return ApiApplicationController.get_all()


@router.post("", summary="Başvuru oluştur", status_code=status.HTTP_201_CREATED)
def api_create_application(data: ApplicationCreate):
    return ApiApplicationController.create(data)


@router.get("/{application_id}", summary="Başvuru detayı")
def api_get_application(application_id: int):
    return ApiApplicationController.get_by_id(application_id)


@router.put("/{application_id}", summary="Başvuruyu tamamen güncelle")
def api_update_application(application_id: int, data: ApplicationUpdate):
    return ApiApplicationController.update(application_id, data)


@router.patch("/{application_id}", summary="Başvuruyu kısmen güncelle")
def api_patch_application(application_id: int, data: ApplicationPatch):
    return ApiApplicationController.patch(application_id, data)


@router.delete("/{application_id}", summary="Başvuruyu sil")
def api_delete_application(application_id: int):
    return ApiApplicationController.delete(application_id)


# ------------- Nested routes: /api/users/{user_id}/applications -------------
@user_nested_router.get("", summary="Kullanıcının başvurularını listele")
def api_list_user_applications(user_id: int):
    return ApiApplicationController.get_by_user(user_id)


@user_nested_router.post(
    "", summary="Kullanıcı adına başvuru oluştur", status_code=status.HTTP_201_CREATED
)
def api_create_user_application(user_id: int, data: UserApplicationCreate):
    return ApiApplicationController.create_for_user(user_id, data)


@user_nested_router.get("/{application_id}", summary="Kullanıcının tek bir başvurusu")
def api_get_user_application(user_id: int, application_id: int):
    return ApiApplicationController.get_user_application(user_id, application_id)


# ---------- Nested routes: /api/job-postings/{job_id}/applications ----------
@job_nested_router.get("", summary="İlana gelen başvuruları listele")
def api_list_job_applications(job_id: int):
    return ApiApplicationController.get_by_job(job_id)


@job_nested_router.post(
    "", summary="İlana başvuru oluştur", status_code=status.HTTP_201_CREATED
)
def api_create_job_application(job_id: int, data: JobApplicationCreate):
    return ApiApplicationController.create_for_job(job_id, data)


@job_nested_router.get("/{application_id}", summary="İlana gelen tek bir başvuru")
def api_get_job_application(job_id: int, application_id: int):
    return ApiApplicationController.get_job_application(job_id, application_id)
