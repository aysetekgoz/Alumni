from typing import Any, Dict, List, Optional, Union
from fastapi import APIRouter, HTTPException, status

from models.user import User, UserCreate, UserUpdate, UserPatch

# /api/users yoluna bağlı router (Swagger'da "ApiUser" grubu altında gösterilir)
router = APIRouter(prefix="/api/users", tags=["ApiUser"])


class ApiUserController:
    """
    ApiUserController — /api/users yoluna bağlı bağımsız REST API kontrolcüsü.
    UserController'dan tamamen bağımsızdır, miras almaz.
    Aynı CRUD işlemlerini kendi içinde ayrı ayrı tanımlar ve aynı model katmanını (User) çağırır.
    """

    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        """Kullanıcıları listeler (model katmanını çağırır)."""
        return User.get_all()

    @classmethod
    def get_by_id(cls, user_id: int) -> Dict[str, Any]:
        """ID'ye göre tekil kullanıcı getirir veya 404 fırlatır."""
        user = User.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Kullanıcı bulunamadı"
            )
        return user

    @classmethod
    def create(cls, data: Union[Dict[str, Any], UserCreate]) -> Dict[str, Any]:
        """Yeni kullanıcı oluşturur ve 201 yanıt formatı döner."""
        new_user = User.create(data)
        return {
            "message": "Kullanıcı başarıyla oluşturuldu",
            "user": new_user
        }

    @classmethod
    def update(cls, user_id: int, data: Union[Dict[str, Any], UserUpdate]) -> Dict[str, Any]:
        """Kullanıcı bilgilerini tamamen günceller (PUT) veya 404 fırlatır."""
        updated_user = User.update(user_id, data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Kullanıcı bulunamadı"
            )
        return {
            "message": "Kullanıcı bilgileri tamamen güncellendi (PUT)",
            "user": updated_user
        }

    @classmethod
    def patch(cls, user_id: int, data: Union[Dict[str, Any], UserPatch]) -> Dict[str, Any]:
        """Kullanıcı bilgilerini kısmen günceller (PATCH) veya 404 fırlatır."""
        user = User.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Kullanıcı bulunamadı"
            )

        if hasattr(data, "model_dump"):
            update_data = data.model_dump(exclude_unset=True)
        elif isinstance(data, dict):
            update_data = {k: v for k, v in data.items() if v is not None}
        else:
            raise ValueError("Unsupported data format for patch")

        if not update_data:
            return {
                "message": "Güncellenecek herhangi bir alan gönderilmedi",
                "user": user
            }

        updated_user = User.patch(user_id, data)
        return {
            "message": "Kullanıcı bilgileri kısmen güncellendi (PATCH)",
            "user": updated_user
        }

    @classmethod
    def delete(cls, user_id: int) -> Dict[str, Any]:
        """Kullanıcı kaydını siler veya 404 fırlatır."""
        deleted_user = User.delete(user_id)
        if not deleted_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Kullanıcı bulunamadı"
            )
        return {
            "message": "Kullanıcı başarıyla silindi",
            "deleted_user": deleted_user
        }


# ====================================================
# /api/users Rotaları (ApiUserController CRUD İşlemleri)
# ====================================================

@router.get("", summary="Tüm Kullanıcıları Listele (API)")
def get_users():
    """Tüm kullanıcıları JSON listesi olarak döner."""
    return ApiUserController.get_all()


@router.get("/{user_id}", summary="Kullanıcı Detayını Getir (API)")
def get_user_by_id(user_id: int):
    """Belirtilen ID'ye sahip kullanıcıyı getirir."""
    return ApiUserController.get_by_id(user_id)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Yeni Kullanıcı Oluştur (API)")
def create_user(user: UserCreate):
    """Yeni bir kullanıcı kaydı oluşturur."""
    return ApiUserController.create(user)


@router.put("/{user_id}", summary="Kullanıcıyı Tamamen Güncelle (API PUT)")
def update_user(user_id: int, user_data: UserUpdate):
    """Kullanıcı bilgilerini tamamen günceller."""
    return ApiUserController.update(user_id, user_data)


@router.patch("/{user_id}", summary="Kullanıcıyı Kısmen Güncelle (API PATCH)")
def patch_user(user_id: int, user_data: UserPatch):
    """Kullanıcı bilgilerini kısmen günceller."""
    return ApiUserController.patch(user_id, user_data)


@router.delete("/{user_id}", summary="Kullanıcıyı Sil (API)")
def delete_user(user_id: int):
    """Kullanıcı kaydını siler."""
    return ApiUserController.delete(user_id)
