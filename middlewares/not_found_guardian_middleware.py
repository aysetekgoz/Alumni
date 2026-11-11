import json
from typing import Callable
from urllib.parse import urlencode

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from middlewares.error_logger import write_error_log


class NotFoundGuardianMiddleware(BaseHTTPMiddleware):
    """
    404 Guardian Middleware:
    Uygulamada oluşan tüm 404 (Not Found) yanıtlarını yakalar, hatayı
    logs/error.logs dosyasına kaydeder ve:
    - Web / tarayıcı isteklerini genel '/404' sayfasına (reason bilgisiyle) yönlendirir (redirect),
    - JSON / API istekleri (/api/... ve Accept: application/json) için doğrudan JSON yanıtı döner.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        path = request.url.path

        # Zaten /404 genel hata sayfası çağrıldıysa sonsuz döngüye girmemek için yanıtı doğrudan döndür:
        if path == "/404" or response.status_code != status.HTTP_404_NOT_FOUND:
            return response

        body_bytes = b"".join([chunk async for chunk in response.body_iterator])
        original_detail = None

        if body_bytes:
            try:
                payload = json.loads(body_bytes.decode("utf-8"))
                if isinstance(payload, dict):
                    original_detail = payload.get("detail")
            except Exception:
                original_detail = None

        method = request.method

        # Starlette/FastAPI tanımsız bir route çağrıldığında varsayılan olarak "Not Found" döner.
        # Controller'lar ise kayıt bulunamadığında özel mesaj döner (örn. "Kullanıcı bulunamadı").
        if not original_detail or original_detail == "Not Found":
            reason = f"'{method} {path}' rotası sistemde tanımlı değil (Route not found)."
            detail = reason
        else:
            reason = f"{original_detail} ('{method} {path}' isteğinde aranan kayıt mevcut değil)."
            detail = original_detail

        write_error_log(
            method=method,
            path=path,
            status_code=status.HTTP_404_NOT_FOUND,
            reason=reason,
        )

        accept = request.headers.get("accept", "")
        wants_json = path.startswith("/api") and "text/html" not in accept

        if wants_json:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "error": "Not Found",
                    "reason": reason,
                    "detail": detail,
                    "method": method,
                    "path": path,
                },
            )

        # Geçersiz web/tarayıcı isteklerini genel /404 sayfasına yönlendir (redirect):
        query_string = urlencode({"path": path, "method": method, "reason": reason})
        return RedirectResponse(
            url=f"/404?{query_string}",
            status_code=status.HTTP_302_FOUND,
        )
