import json
import traceback
from typing import Callable

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from middlewares.error_logger import write_error_log
from views.announcement_view import templates


class ServerErrorGuardianMiddleware(BaseHTTPMiddleware):
    """
    5xx Guardian Middleware:
    Uygulamada oluşan tüm 500-599 (5xx) sunucu hatalarını ve yakalanmamış
    istisnaları (unhandled exceptions) yakalar; hata detaylarını logs/error.logs
    dosyasına yazar ve hatanın nedenini ('reason') açıklayan standart bir
    HTML (500.html) veya JSON yanıtı döner.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        path = request.url.path
        method = request.method

        try:
            response = await call_next(request)
        except Exception as exc:
            error_type = type(exc).__name__
            error_msg = str(exc) or "Beklenmeyen sunucu hatası"
            reason = f"Sunucu hatası ({error_type}): {error_msg} ('{method} {path}' işlenirken oluştu)."
            tb_lines = traceback.format_tb(exc.__traceback__)
            short_tb = "".join(tb_lines[-3:]) + "".join(
                traceback.format_exception_only(type(exc), exc)
            )
            write_error_log(
                method=method,
                path=path,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                reason=reason,
                traceback_str=short_tb,
            )
            return self._build_5xx_response(
                request=request,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                reason=reason,
                detail=error_msg,
            )

        if not (500 <= response.status_code < 600):
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

        if original_detail:
            reason = f"{original_detail} ('{method} {path}' isteği sırasında {response.status_code} sunucu hatası oluştu)."
            detail = original_detail
        else:
            reason = f"'{method} {path}' isteği işlenirken {response.status_code} sunucu hatası oluştu (Internal Server Error)."
            detail = reason

        write_error_log(
            method=method,
            path=path,
            status_code=response.status_code,
            reason=reason,
        )

        return self._build_5xx_response(
            request=request,
            status_code=response.status_code,
            reason=reason,
            detail=detail,
        )

    @staticmethod
    def _build_5xx_response(
        request: Request, status_code: int, reason: str, detail: str
    ) -> Response:
        path = request.url.path
        method = request.method
        accept = request.headers.get("accept", "")
        wants_json = path.startswith("/api") and "text/html" not in accept

        payload = {
            "status_code": status_code,
            "error": "Internal Server Error",
            "reason": reason,
            "detail": detail,
            "method": method,
            "path": path,
        }

        if wants_json:
            return JSONResponse(status_code=status_code, content=payload)

        return templates.TemplateResponse(
            request,
            "500.html",
            payload,
            status_code=status_code,
        )
