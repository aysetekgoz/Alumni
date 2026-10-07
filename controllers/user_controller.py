from typing import Any, Dict, List, Optional, Union
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import HTMLResponse

from models.user import User, UserCreate, UserUpdate, UserPatch
from views import UserView

# /users yoluna bağlı router (Swagger'da "User" grubu altında gösterilir)
router = APIRouter(prefix="/users", tags=["User"])


class UserController:
    """
    UserController — /users yoluna bağlı kullanıcı kontrolcüsü.
    CRUD işlemlerini veri katmanındaki (User modeli) fonksiyonları çağırarak yürütür,
    sunum için View katmanını (UserView) kullanır. Kendisi veri tutmaz.
    """

    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        """[R - Read All] Kullanıcıları listeler (model katmanını çağırır)."""
        return User.get_all()

    @classmethod
    def get_by_id(cls, user_id: int) -> Optional[Dict[str, Any]]:
        """[R - Read One] ID'ye göre tekil kullanıcı getirir (model katmanını çağırır)."""
        return User.get_by_id(user_id)

    @classmethod
    def create(cls, data: Union[Dict[str, Any], UserCreate]) -> Dict[str, Any]:
        """[C - Create] Yeni kullanıcı oluşturur (model katmanını çağırır)."""
        return User.create(data)

    @classmethod
    def update(cls, user_id: int, data: Union[Dict[str, Any], UserUpdate]) -> Optional[Dict[str, Any]]:
        """[U - Update] Kullanıcı bilgilerini tamamen günceller (model katmanını çağırır)."""
        return User.update(user_id, data)

    @classmethod
    def patch(cls, user_id: int, data: Union[Dict[str, Any], UserPatch]) -> Optional[Dict[str, Any]]:
        """[U - Patch] Kullanıcı bilgilerini kısmen günceller (model katmanını çağırır)."""
        return User.patch(user_id, data)

    @classmethod
    def delete(cls, user_id: int) -> Optional[Dict[str, Any]]:
        """[D - Delete] Kullanıcıyı siler (model katmanını çağırır)."""
        return User.delete(user_id)


# =========================================================================
# Web Arayüzü Üzerinden Tüm CRUD Operasyonları (View Layer Destekli)
# =========================================================================

# 1. READ ALL (R) — GET /users
@router.get(
    "",
    summary="Tüm Mezunları Listele (Read - R)",
    response_class=HTMLResponse,
)
def list_users(request: Request):
    """
    [R - Read] Tüm kullanıcıları Model katmanından çeker ve
    View katmanı (UserView) üzerinden HTML listesi olarak sunar.
    """
    if "application/json" in request.headers.get("accept", ""):
        return UserController.get_all()
    users = UserController.get_all()
    return UserView.render_list(request, users)


# 2. READ ONE (R) — GET /users/{user_id}
@router.get(
    "/{user_id}",
    summary="Tekil Mezun Detayı (Read - R)",
    response_class=HTMLResponse,
)
def get_user_detail(user_id: int, request: Request):
    """
    [R - Read] Belirli bir ID'ye sahip kullanıcıyı getirir.
    """
    user = UserController.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kullanıcı bulunamadı"
        )
    if "application/json" in request.headers.get("accept", ""):
        return user
    return UserView.render_list(
        request,
        [user],
        message=f"Seçilen Mezun: {user['first_name']} {user['last_name']}",
    )


# 3. CREATE (C) — POST /users
@router.post(
    "",
    summary="Yeni Mezun Oluştur (Create - C)",
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(request: Request):
    """
    [C - Create] HTML Form veya JSON üzerinden gelen veriyi alarak
    Model katmanında yeni kullanıcı oluşturur ve View katmanını günceller.
    """
    content_type = request.headers.get("content-type", "")
    new_user = None

    if "application/json" in content_type:
        body = await request.json()
        new_user = UserController.create(body)
    elif "application/x-www-form-urlencoded" in content_type:
        raw_body = await request.body()
        from urllib.parse import parse_qs
        parsed = parse_qs(raw_body.decode("utf-8"))
        form_dict = {
            "first_name": parsed.get("first_name", [""])[0],
            "last_name": parsed.get("last_name", [""])[0],
            "email": parsed.get("email", [""])[0],
            "graduation_year": int(parsed.get("graduation_year", ["2026"])[0] or 2026),
            "department": parsed.get("department", [""])[0],
        }
        new_user = UserController.create(form_dict)
    else:
        try:
            body = await request.json()
            new_user = UserController.create(body)
        except Exception:
            raw_body = await request.body()
            from urllib.parse import parse_qs
            parsed = parse_qs(raw_body.decode("utf-8"))
            form_dict = {
                "first_name": parsed.get("first_name", [""])[0],
                "last_name": parsed.get("last_name", [""])[0],
                "email": parsed.get("email", [""])[0],
                "graduation_year": int(parsed.get("graduation_year", ["2026"])[0] or 2026),
                "department": parsed.get("department", [""])[0],
            }
            new_user = UserController.create(form_dict)

    users = UserController.get_all()
    message = (
        f"'{new_user['first_name']} {new_user['last_name']}' başarıyla oluşturuldu!"
        if new_user
        else "Yeni mezun kaydı başarıyla eklendi."
    )
    return UserView.render_list(
        request,
        users,
        message=message,
        status_code=status.HTTP_201_CREATED,
    )


# 4. UPDATE (U) — POST /users/{user_id}/update ve PUT /users/{user_id}
@router.post(
    "/{user_id}/update",
    summary="Mezun Bilgilerini Güncelle (Form Update - U)",
    response_class=HTMLResponse,
)
@router.put(
    "/{user_id}",
    summary="Mezun Bilgilerini Güncelle (PUT Update - U)",
    response_class=HTMLResponse,
)
async def update_user(user_id: int, request: Request):
    """
    [U - Update] Web arayüzünden veya API'den gelen verilerle
    belirtilen ID'deki kullanıcıyı günceller ve View katmanını tazeler.
    """
    content_type = request.headers.get("content-type", "")
    update_data = {}

    if "application/json" in content_type:
        update_data = await request.json()
    else:
        raw_body = await request.body()
        from urllib.parse import parse_qs
        parsed = parse_qs(raw_body.decode("utf-8"))
        update_data = {
            "first_name": parsed.get("first_name", [""])[0],
            "last_name": parsed.get("last_name", [""])[0],
            "email": parsed.get("email", [""])[0],
            "graduation_year": int(parsed.get("graduation_year", ["2026"])[0] or 2026),
            "department": parsed.get("department", [""])[0],
        }

    updated = UserController.update(user_id, update_data)
    users = UserController.get_all()
    if updated:
        msg = f"#{user_id} numaralı mezun bilgileri başarıyla güncellendi!"
    else:
        msg = f"Güncellenecek kullanıcı bulunamadı (ID #{user_id})."
    return UserView.render_list(request, users, message=msg)


# 5. DELETE (D) — POST /users/{user_id}/delete ve DELETE /users/{user_id}
@router.post(
    "/{user_id}/delete",
    summary="Mezunu Sil (Form Delete - D)",
    response_class=HTMLResponse,
)
@router.delete(
    "/{user_id}",
    summary="Mezunu Sil (DELETE - D)",
    response_class=HTMLResponse,
)
def delete_user(user_id: int, request: Request):
    """
    [D - Delete] Web arayüzündeki silme butonundan veya API'den gelen
    istekle kullanıcıyı Model üzerinden siler ve View katmanını günceller.
    """
    deleted = UserController.delete(user_id)
    users = UserController.get_all()
    if deleted:
        msg = f"'{deleted['first_name']} {deleted['last_name']}' başarıyla silindi!"
    else:
        msg = f"Silinecek kullanıcı bulunamadı (ID #{user_id})."
    return UserView.render_list(request, users, message=msg)
