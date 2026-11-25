from urllib.parse import parse_qs
from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from models.user import User
from views import UserView

router = APIRouter(tags=["Auth"])

ALLOWED_REGISTER_ROLES = ("alumni", "student", "academic", "staff", "admin")


@router.get(
    "/register",
    summary="Kayıt Sayfası (Register Form)",
    response_class=HTMLResponse,
)
def get_register_page(request: Request):
    """Kayıt formunu (GET /register) görüntüler."""
    return UserView.render_register(request)


@router.post(
    "/register",
    summary="Yeni Kullanıcı Kaydı (Register)",
    response_class=HTMLResponse,
)
async def submit_register(request: Request):
    """
    Kayıt formundan (POST /register) gelen verileri doğrular ve kullanıcıyı oluşturur.

    TODO (Service Layer - Şimdilik Pasif):
    Hibrit E-posta + Servis Katmanında Onay Akışı (services/auth_service.py) henüz
    aktif değildir. İlerleyen aşamada aşağıdaki kurallar servis katmanına taşınacaktır:
      1. Kurumsal/öğrenci e-postası (@ogr.iu.edu.tr, @istanbul.edu.tr) -> is_active = True
      2. Kişisel e-posta (gmail.com vb.) -> is_active = False (admin onayı bekler)
      3. Şifre hashleme (password_hash) ve users.role ('student' / 'alumni') kaydı
    """
    raw_body = await request.body()
    parsed = parse_qs(raw_body.decode("utf-8"))

    first_name = parsed.get("first_name", [""])[0].strip()
    last_name = parsed.get("last_name", [""])[0].strip()
    email = parsed.get("email", [""])[0].strip().lower()
    role = parsed.get("role", ["alumni"])[0].strip()
    department = parsed.get("department", [""])[0].strip()
    grad_year_raw = parsed.get("graduation_year", [""])[0].strip()
    password = parsed.get("password", [""])[0]
    password_confirm = parsed.get("password_confirm", [""])[0]

    form_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "role": role,
        "department": department,
        "graduation_year": grad_year_raw,
    }

    if not all([first_name, last_name, email, department, password]):
        return UserView.render_register(
            request,
            error="Lütfen tüm zorunlu alanları doldurun.",
            form_data=form_data,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if role not in ALLOWED_REGISTER_ROLES:
        return UserView.render_register(
            request,
            error="Geçersiz kullanıcı tipi seçildi.",
            form_data=form_data,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if role in ("alumni", "student") and not grad_year_raw:
        return UserView.render_register(
            request,
            error="Öğrenci ve mezun rolleri için mezuniyet yılı zorunludur.",
            form_data=form_data,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if grad_year_raw:
        try:
            graduation_year = int(grad_year_raw)
        except ValueError:
            return UserView.render_register(
                request,
                error="Mezuniyet yılı geçerli bir sayı olmalıdır.",
                form_data=form_data,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not (1900 <= graduation_year <= 2100):
            return UserView.render_register(
                request,
                error="Mezuniyet yılı 1900 ile 2100 arasında olmalıdır.",
                form_data=form_data,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    else:
        graduation_year = None

    if len(password) < 6:
        return UserView.render_register(
            request,
            error="Şifre en az 6 karakter olmalıdır.",
            form_data=form_data,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if password != password_confirm:
        return UserView.render_register(
            request,
            error="Şifreler birbiriyle eşleşmiyor.",
            form_data=form_data,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if User.get_by_email(email):
        return UserView.render_register(
            request,
            error=f"'{email}' adresi ile zaten kayıtlı bir kullanıcı bulunuyor.",
            form_data=form_data,
            status_code=status.HTTP_409_CONFLICT,
        )

    created = User.create(
        {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "role": role,
            "graduation_year": graduation_year,
            "department": department,
        }
    )

    response = RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="alumni_user_id", value=str(created["id"]), httponly=True, samesite="lax")
    return response


@router.get(
    "/login",
    summary="Giriş Sayfası (Login Form)",
    response_class=HTMLResponse,
)
def get_login_page(request: Request):
    """Giriş formunu (GET /login) görüntüler."""
    return UserView.render_login(request)


@router.post(
    "/login",
    summary="Kullanıcı Girişi (Login)",
    response_class=HTMLResponse,
)
async def submit_login(request: Request):
    """
    Giriş formundan (POST /login) gelen e-posta ve şifreyi doğrular,
    oturum çerezini (cookie) ayarlayarak kullanıcıyı sisteme (/home) yönlendirir.

    TODO (Service Layer - Şimdilik Pasif):
    Üniversite üyelik doğrulaması (öğrenci/akademisyen/mezun domain kontrolü)
    ve is_active onay akışı servis katmanı (services/auth_service.py)
    eklendiğinde aktif edilecektir. Şu an yalnızca e-posta + şifre eşleşmesi yapılır.
    """
    raw_body = await request.body()
    parsed = parse_qs(raw_body.decode("utf-8"))

    email = parsed.get("email", [""])[0].strip().lower()
    password = parsed.get("password", [""])[0]
    form_data = {"email": email}

    if not email or not password:
        return UserView.render_login(
            request,
            error="Lütfen e-posta ve şifre alanlarını doldurun.",
            form_data=form_data,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    user = User.authenticate(email, password)
    if not user:
        return UserView.render_login(
            request,
            error="E-posta adresi veya şifre hatalı.",
            form_data=form_data,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    response = RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="alumni_user_id", value=str(user["id"]), httponly=True, samesite="lax")
    return response


@router.get(
    "/logout",
    summary="Sistemden Çıkış (Logout)",
)
@router.post(
    "/logout",
    summary="Sistemden Çıkış (Logout POST)",
)
def logout():
    """Oturum çerezini temizler ve kullanıcıyı giriş sayfasına (/login) yönlendirir."""
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="alumni_user_id")
    return response
