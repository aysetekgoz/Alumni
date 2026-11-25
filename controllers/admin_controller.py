from urllib.parse import parse_qs, quote
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from models.announcement import Announcement
from models.application import Application
from models.job_posting import JobPosting
from models.user import User
from views.announcement_view import templates

router = APIRouter(prefix="/admin", tags=["Admin"])

VALID_ROLES = ("admin", "staff", "academic", "student", "alumni")
VALID_APP_STATUSES = ("pending", "reviewed", "accepted", "rejected")


def _require_admin(request: Request) -> dict:
    current_user = getattr(request.state, "current_user", None)
    if not current_user or current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu alana yalnızca admin rolüne sahip kullanıcılar erişebilir.",
        )
    return current_user


def _redirect_admin(msg: str) -> RedirectResponse:
    return RedirectResponse(
        url=f"/admin?msg={quote(msg)}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("", summary="Admin Yönetim Paneli", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    current_user = _require_admin(request)
    users = User.get_all()
    announcements = Announcement.get_all()
    jobs = JobPosting.get_all()
    applications = Application.get_all()
    msg = request.query_params.get("msg")

    return templates.TemplateResponse(
        request,
        "admin.html",
        {
            "current_user": current_user,
            "users": users,
            "announcements": announcements,
            "jobs": jobs,
            "applications": applications,
            "roles": VALID_ROLES,
            "app_statuses": VALID_APP_STATUSES,
            "message": msg,
        },
    )


@router.post("/users/create", summary="Admin: Yeni Kullanıcı Oluştur")
async def admin_create_user(request: Request):
    _require_admin(request)
    parsed = parse_qs((await request.body()).decode("utf-8"))

    first_name = parsed.get("first_name", [""])[0].strip()
    last_name = parsed.get("last_name", [""])[0].strip()
    email = parsed.get("email", [""])[0].strip().lower()
    role = parsed.get("role", ["alumni"])[0].strip()
    department = parsed.get("department", [""])[0].strip()
    grad_year_raw = parsed.get("graduation_year", [""])[0].strip()
    password = parsed.get("password", [""])[0]

    if not all([first_name, last_name, email, department, password]) or role not in VALID_ROLES:
        return _redirect_admin("Hata: Zorunlu alanları ve geçerli bir rolü doldurun.")

    if User.get_by_email(email):
        return _redirect_admin(f"Hata: '{email}' zaten kayıtlı.")

    graduation_year = int(grad_year_raw) if grad_year_raw.isdigit() else None
    User.create(
        {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "role": role,
            "is_active": True,
            "graduation_year": graduation_year,
            "department": department,
        }
    )
    return _redirect_admin(f"Kullanıcı oluşturuldu: {first_name} {last_name} ({role})")


@router.post("/users/{user_id}/update", summary="Admin: Kullanıcı Rol ve Durum Güncelle")
async def admin_update_user(user_id: int, request: Request):
    _require_admin(request)
    parsed = parse_qs((await request.body()).decode("utf-8"))
    role = parsed.get("role", ["alumni"])[0].strip()
    is_active = parsed.get("is_active", ["true"])[0].strip().lower() == "true"

    if role not in VALID_ROLES:
        return _redirect_admin("Hata: Geçersiz rol.")

    updated = User.patch(user_id, {"role": role, "is_active": is_active})
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kullanıcı bulunamadı")

    durum = "Aktif" if is_active else "Pasif"
    return _redirect_admin(f"Kullanıcı #{user_id} güncellendi → Rol: {role}, Durum: {durum}")


@router.post("/users/{user_id}/delete", summary="Admin: Kullanıcı Sil")
def admin_delete_user(user_id: int, request: Request):
    current_user = _require_admin(request)
    if current_user["id"] == user_id:
        return _redirect_admin("Hata: Kendi aktif admin hesabınızı silemezsiniz.")

    deleted = User.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kullanıcı bulunamadı")
    return _redirect_admin(f"Kullanıcı #{user_id} ({deleted['email']}) silindi.")


@router.post("/jobs/{job_id}/toggle", summary="Admin: İlan Aktif/Pasif Değiştir")
def admin_toggle_job(job_id: int, request: Request):
    _require_admin(request)
    job = JobPosting.get_by_id(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="İş ilanı bulunamadı")

    new_state = not bool(job.get("is_active", True))
    JobPosting.patch(job_id, {"is_active": new_state})
    return _redirect_admin(f"İlan #{job_id} durumu → {'Aktif' if new_state else 'Pasif'}")


@router.post("/jobs/{job_id}/delete", summary="Admin: İlan Sil")
def admin_delete_job(job_id: int, request: Request):
    _require_admin(request)
    deleted = JobPosting.delete(job_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="İş ilanı bulunamadı")
    return _redirect_admin(f"İş ilanı #{job_id} silindi.")


@router.post("/announcements/{announcement_id}/delete", summary="Admin: Duyuru Sil")
def admin_delete_announcement(announcement_id: int, request: Request):
    _require_admin(request)
    deleted = Announcement.delete(announcement_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Duyuru bulunamadı")
    return _redirect_admin(f"Duyuru #{announcement_id} silindi.")


@router.post("/applications/{application_id}/status", summary="Admin: Başvuru Durumu Güncelle")
async def admin_update_application_status(application_id: int, request: Request):
    _require_admin(request)
    parsed = parse_qs((await request.body()).decode("utf-8"))
    new_status = parsed.get("status", ["pending"])[0].strip()

    if new_status not in VALID_APP_STATUSES:
        return _redirect_admin("Hata: Geçersiz başvuru durumu.")

    updated = Application.patch(application_id, {"status": new_status})
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Başvuru bulunamadı")
    return _redirect_admin(f"Başvuru #{application_id} durumu → {new_status}")


@router.post("/applications/{application_id}/delete", summary="Admin: Başvuru Sil")
def admin_delete_application(application_id: int, request: Request):
    _require_admin(request)
    deleted = Application.delete(application_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Başvuru bulunamadı")
    return _redirect_admin(f"Başvuru #{application_id} silindi.")
