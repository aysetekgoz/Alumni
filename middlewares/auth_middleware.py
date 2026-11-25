from typing import Callable, Optional

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from models.user import User


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Auth Middleware:
    Her istekte 'alumni_user_id' oturum çerezini kontrol eder ve geçerli
    kullanıcıyı `request.state.current_user` üzerine ekler.
    Oturum açmamış istekleri:
    - Web / tarayıcı rotalarında '/login' sayfasına yönlendirir (302),
    - '/api/...' rotalarında 401 Unauthorized JSON yanıtı döner.
    """

    PUBLIC_PATHS = {
        "/",
        "/register",
        "/login",
        "/logout",
        "/404",
        "/api/health",
        "/api/swagger",
        "/docs",
        "/openapi.json",
        "/redoc",
    }
    PUBLIC_PREFIXES = ("/static/",)

    @classmethod
    def _is_public(cls, path: str) -> bool:
        if path in cls.PUBLIC_PATHS:
            return True
        return any(path.startswith(prefix) for prefix in cls.PUBLIC_PREFIXES)

    @staticmethod
    def _resolve_user(request: Request) -> Optional[dict]:
        user_id_raw = request.cookies.get("alumni_user_id")
        if not user_id_raw or not user_id_raw.isdigit():
            return None
        return User.get_by_id(int(user_id_raw))

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        path = request.url.path
        current_user = self._resolve_user(request)
        request.state.current_user = current_user

        if self._is_public(path) or current_user is not None:
            return await call_next(request)

        accept = request.headers.get("accept", "")
        wants_json = path.startswith("/api") and "text/html" not in accept
        if wants_json:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "status_code": status.HTTP_401_UNAUTHORIZED,
                    "error": "Unauthorized",
                    "detail": "Bu işlem için giriş yapmanız gerekiyor.",
                    "path": path,
                },
            )

        response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
        if request.cookies.get("alumni_user_id"):
            response.delete_cookie(key="alumni_user_id")
        return response
