from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, status

from models.job_posting import (
    JobPosting,
    JobPostingCreate,
    JobPostingPatch,
    JobPostingUpdate,
)
from models.user import User

# Direct routes: the resource is addressed on its own.      /api/job-postings
router = APIRouter(prefix="/api/job-postings", tags=["ApiJobPosting"])
# Nested routes: the resource is addressed through its parent user.
#                                                  /api/users/{user_id}/job-postings
nested_router = APIRouter(
    prefix="/api/users/{user_id}/job-postings", tags=["ApiUserJobPosting"]
)

NOT_FOUND = "İş ilanı bulunamadı"
USER_NOT_FOUND = "Kullanıcı bulunamadı"


class ApiJobPostingController:
    """JSON REST controller for job postings (direct and nested routes)."""

    # ---- direct ----
    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        return JobPosting.get_all()

    @classmethod
    def get_by_id(cls, job_id: int) -> Dict[str, Any]:
        item = JobPosting.get_by_id(job_id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
        return item

    @classmethod
    def create(cls, data: JobPostingCreate) -> Dict[str, Any]:
        # posted_by FK violation is turned into an error response by main.py's IntegrityError handler.
        return JobPosting.create(data)

    @classmethod
    def update(cls, job_id: int, data: JobPostingUpdate) -> Dict[str, Any]:
        item = JobPosting.update(job_id, data)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
        return item

    @classmethod
    def patch(cls, job_id: int, data: JobPostingPatch) -> Dict[str, Any]:
        item = JobPosting.patch(job_id, data)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
        return item

    @classmethod
    def delete(cls, job_id: int) -> Dict[str, Any]:
        item = JobPosting.delete(job_id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
        return {"message": "İş ilanı silindi", "job_posting": item}

    # ---- nested (parent: user) ----
    @staticmethod
    def _require_user(user_id: int) -> None:
        if User.get_by_id(user_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND)

    @classmethod
    def get_by_user(cls, user_id: int) -> List[Dict[str, Any]]:
        cls._require_user(user_id)
        return JobPosting.get_by_user(user_id)

    @classmethod
    def get_user_posting(cls, user_id: int, job_id: int) -> Dict[str, Any]:
        cls._require_user(user_id)
        item = JobPosting.get_by_id(job_id)
        # A posting that belongs to another user is not found under this user.
        if item is None or item["posted_by"] != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
        return item

    @classmethod
    def create_for_user(cls, user_id: int, data: JobPostingCreate) -> Dict[str, Any]:
        cls._require_user(user_id)
        payload = data.model_dump()
        payload["posted_by"] = user_id  # taken from the URL, not from the body
        return JobPosting.create(payload)


# ---------------- Direct routes: /api/job-postings ----------------
@router.get("", summary="Tüm iş ilanlarını listele")
def api_list_job_postings():
    return ApiJobPostingController.get_all()


@router.post("", summary="İş ilanı oluştur", status_code=status.HTTP_201_CREATED)
def api_create_job_posting(data: JobPostingCreate):
    return ApiJobPostingController.create(data)


@router.get("/{job_id}", summary="İş ilanı detayı")
def api_get_job_posting(job_id: int):
    return ApiJobPostingController.get_by_id(job_id)


@router.put("/{job_id}", summary="İş ilanını tamamen güncelle")
def api_update_job_posting(job_id: int, data: JobPostingUpdate):
    return ApiJobPostingController.update(job_id, data)


@router.patch("/{job_id}", summary="İş ilanını kısmen güncelle")
def api_patch_job_posting(job_id: int, data: JobPostingPatch):
    return ApiJobPostingController.patch(job_id, data)


@router.delete("/{job_id}", summary="İş ilanını sil")
def api_delete_job_posting(job_id: int):
    return ApiJobPostingController.delete(job_id)


# ------------- Nested routes: /api/users/{user_id}/job-postings -------------
@nested_router.get("", summary="Kullanıcının iş ilanlarını listele")
def api_list_user_job_postings(user_id: int):
    return ApiJobPostingController.get_by_user(user_id)


@nested_router.post(
    "", summary="Kullanıcı adına iş ilanı oluştur", status_code=status.HTTP_201_CREATED
)
def api_create_user_job_posting(user_id: int, data: JobPostingCreate):
    return ApiJobPostingController.create_for_user(user_id, data)


@nested_router.get("/{job_id}", summary="Kullanıcının tek bir iş ilanı")
def api_get_user_job_posting(user_id: int, job_id: int):
    return ApiJobPostingController.get_user_posting(user_id, job_id)
