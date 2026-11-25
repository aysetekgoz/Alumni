from urllib.parse import parse_qs, quote
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from models.application import Application
from models.job_posting import JobPosting
from models.user import User
from views.announcement_view import templates

router = APIRouter(tags=["Portal"])

MY_JOBS_ROLES = ("alumni", "academic", "staff", "admin")
MY_APPS_ROLES = ("student", "alumni", "admin")
VALID_APP_STATUSES = ("pending", "reviewed", "accepted", "rejected")


def _require_user(request: Request) -> dict:
    current_user = getattr(request.state, "current_user", None)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bu sayfa için giriş yapmanız gerekiyor.",
        )
    return current_user


# =========================================================================
# 1. Profilim (/profile) — Tüm Giriş Yapmış Roller
# =========================================================================

@router.get("/profile", summary="Kullanıcı Profil Sayfası", response_class=HTMLResponse)
def get_profile(request: Request):
    current_user = _require_user(request)
    return templates.TemplateResponse(
        request,
        "profile.html",
        {
            "current_user": current_user,
            "message": request.query_params.get("msg"),
            "error": request.query_params.get("err"),
        },
    )


@router.post("/profile", summary="Kullanıcı Profilini Güncelle", response_class=HTMLResponse)
async def update_profile(request: Request):
    current_user = _require_user(request)
    parsed = parse_qs((await request.body()).decode("utf-8"))

    first_name = parsed.get("first_name", [""])[0].strip()
    last_name = parsed.get("last_name", [""])[0].strip()
    email = parsed.get("email", [""])[0].strip().lower()
    department = parsed.get("department", [""])[0].strip()
    grad_year_raw = parsed.get("graduation_year", [""])[0].strip()

    if not all([first_name, last_name, email, department]):
        return RedirectResponse(
            url=f"/profile?err={quote('Lütfen tüm zorunlu alanları doldurun.')}",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    role = current_user.get("role", "alumni")
    if role in ("student", "alumni") and not grad_year_raw:
        return RedirectResponse(
            url=f"/profile?err={quote('Öğrenci ve mezun rolleri için mezuniyet yılı zorunludur.')}",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    graduation_year = None
    if grad_year_raw:
        if not grad_year_raw.isdigit() or not (1900 <= int(grad_year_raw) <= 2100):
            return RedirectResponse(
                url=f"/profile?err={quote('Mezuniyet yılı 1900 ile 2100 arasında olmalıdır.')}",
                status_code=status.HTTP_303_SEE_OTHER,
            )
        graduation_year = int(grad_year_raw)

    existing = User.get_by_email(email)
    if existing and existing["id"] != current_user["id"]:
        return RedirectResponse(
            url=f"/profile?err={quote('Bu e-posta adresi başka bir kullanıcı tarafından kullanılıyor.')}",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    # Not: role ve is_active kullanıcı tarafından değiştirilemez (ddd.md 6.3)
    User.patch(
        current_user["id"],
        {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "department": department,
            "graduation_year": graduation_year,
        },
    )
    return RedirectResponse(
        url=f"/profile?msg={quote('Profil bilgileriniz güncellendi.')}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


# =========================================================================
# 2. Başvurularım (/my-applications) — Öğrenci & Mezun (& Admin)
# =========================================================================

@router.get("/my-applications", summary="Kullanıcının Kendi Başvuruları", response_class=HTMLResponse)
def get_my_applications(request: Request):
    current_user = _require_user(request)
    if current_user.get("role") not in MY_APPS_ROLES:
        detail = "Bu sayfa yalnızca öğrenci, mezun ve admin rolleri içindir."
        if "text/html" in request.headers.get("accept", ""):
            return templates.TemplateResponse(
                request, "403.html", {"current_user": current_user, "detail": detail}, status_code=status.HTTP_403_FORBIDDEN
            )
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

    apps = Application.get_by_user(current_user["id"])
    jobs_by_id = {j["id"]: j for j in JobPosting.get_all()}
    enriched = []
    for ap in apps:
        job = jobs_by_id.get(ap["job_posting_id"], {})
        enriched.append({**ap, "job": job})

    return templates.TemplateResponse(
        request,
        "my_applications.html",
        {
            "current_user": current_user,
            "applications": enriched,
            "message": request.query_params.get("msg"),
        },
    )


@router.post("/my-applications/{application_id}/delete", summary="Kendi Başvurusunu Geri Çek")
def delete_my_application(application_id: int, request: Request):
    current_user = _require_user(request)
    if current_user.get("role") not in MY_APPS_ROLES:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Yetkisiz erişim.")

    ap = Application.get_by_id(application_id)
    if not ap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Başvuru bulunamadı")

    if ap["user_id"] != current_user["id"] and current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Yalnızca kendi başvurunuzu silebilirsiniz.")

    Application.delete(application_id)
    return RedirectResponse(
        url=f"/my-applications?msg={quote('Başvurunuz geri çekildi.')}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


# =========================================================================
# 3. İlanlarım (/my-jobs) — Mezun, Akademisyen, Çalışan, Admin
# =========================================================================

@router.get("/my-jobs", summary="Kullanıcının Kendi İş İlanları ve Gelen Başvurular", response_class=HTMLResponse)
def get_my_jobs(request: Request):
    current_user = _require_user(request)
    if current_user.get("role") not in MY_JOBS_ROLES:
        detail = "Öğrenci rolü iş ilanı yönetimi sayfasına erişemez."
        if "text/html" in request.headers.get("accept", ""):
            return templates.TemplateResponse(
                request, "403.html", {"current_user": current_user, "detail": detail}, status_code=status.HTTP_403_FORBIDDEN
            )
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

    my_jobs = JobPosting.get_by_user(current_user["id"])
    users_by_id = {u["id"]: u for u in User.get_all()}
    jobs_with_apps = []
    for job in my_jobs:
        apps = Application.get_by_job_posting(job["id"])
        enriched_apps = [
            {**ap, "applicant": users_by_id.get(ap["user_id"], {})}
            for ap in apps
        ]
        jobs_with_apps.append({**job, "applications": enriched_apps})

    return templates.TemplateResponse(
        request,
        "my_jobs.html",
        {
            "current_user": current_user,
            "jobs": jobs_with_apps,
            "app_statuses": VALID_APP_STATUSES,
            "message": request.query_params.get("msg"),
            "error": request.query_params.get("err"),
        },
    )


@router.post("/my-jobs/create", summary="Kendi Adına İş İlanı Oluştur")
async def create_my_job(request: Request):
    current_user = _require_user(request)
    if current_user.get("role") not in MY_JOBS_ROLES:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Yetkisiz erişim.")

    parsed = parse_qs((await request.body()).decode("utf-8"))
    title = parsed.get("title", [""])[0].strip()
    company = parsed.get("company", [""])[0].strip()
    city = parsed.get("city", [""])[0].strip() or None
    employment_type = parsed.get("employment_type", ["full_time"])[0].strip()
    description = parsed.get("description", [""])[0].strip() or None
    application_url = parsed.get("application_url", [""])[0].strip() or None

    if not title or not company:
        return RedirectResponse(
            url=f"/my-jobs?err={quote('İlan başlığı ve şirket adı zorunludur.')}",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    JobPosting.create(
        {
            "title": title[:120],
            "company": company,
            "city": city,
            "employment_type": employment_type,
            "description": description,
            "application_url": application_url,
            "is_active": True,
            "posted_by": current_user["id"],
        }
    )
    return RedirectResponse(
        url=f"/my-jobs?msg={quote('Yeni iş ilanınız yayınlandı.')}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post("/my-jobs/{job_id}/toggle", summary="Kendi İlanını Aktif/Pasif Yap")
def toggle_my_job(job_id: int, request: Request):
    current_user = _require_user(request)
    job = JobPosting.get_by_id(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="İş ilanı bulunamadı")

    if job.get("posted_by") != current_user["id"] and current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Yalnızca kendi ilanınızı güncelleyebilirsiniz.")

    new_state = not bool(job.get("is_active", True))
    JobPosting.patch(job_id, {"is_active": new_state})
    return RedirectResponse(
        url=f"/my-jobs?msg={quote('İlan durumu güncellendi.')}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post("/my-jobs/{job_id}/delete", summary="Kendi İlanını Sil")
def delete_my_job(job_id: int, request: Request):
    current_user = _require_user(request)
    job = JobPosting.get_by_id(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="İş ilanı bulunamadı")

    if job.get("posted_by") != current_user["id"] and current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Yalnızca kendi ilanınızı silebilirsiniz.")

    JobPosting.delete(job_id)
    return RedirectResponse(
        url=f"/my-jobs?msg={quote('İlanınız silindi.')}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post("/my-jobs/applications/{application_id}/status", summary="Kendi İlanına Gelen Başvuru Durumunu Güncelle")
async def update_my_job_application_status(application_id: int, request: Request):
    current_user = _require_user(request)
    ap = Application.get_by_id(application_id)
    if not ap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Başvuru bulunamadı")

    job = JobPosting.get_by_id(ap["job_posting_id"])
    if not job or (job.get("posted_by") != current_user["id"] and current_user.get("role") != "admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Yalnızca kendi ilanınıza gelen başvuruları güncelleyebilirsiniz.")

    parsed = parse_qs((await request.body()).decode("utf-8"))
    new_status = parsed.get("status", ["pending"])[0].strip()
    if new_status in VALID_APP_STATUSES:
        Application.patch(application_id, {"status": new_status})

    return RedirectResponse(
        url=f"/my-jobs?msg={quote('Başvuru durumu güncellendi.')}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
