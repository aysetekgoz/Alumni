import time
from datetime import datetime
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from middlewares.error_logger import write_error_log


class LoggerMiddleware(BaseHTTPMiddleware):
    """
    HTTP isteklerini terminale loglayan middleware.
    Format: time method route restype duration
    Örnek:  10:20:30  POST /user 201 18 ms
    Ayrıca 404 ve 5xx dışındaki diğer hata durum kodlarını (örn. 400, 409, 422)
    logs/error.logs dosyasına da yazar.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start_time) * 1000)
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(
            f"{timestamp}  {request.method} {request.url.path} {response.status_code} {duration_ms} ms",
            flush=True,
        )

        # 404 ve 5xx hataları kendi Guardian middleware'leri tarafından detaylıca loglanır.
        # Diğer 4xx hatalarını (örn. 409 Conflict, 422 Validation Error) da error.logs'a kaydet:
        if 400 <= response.status_code < 500 and response.status_code != 404:
            write_error_log(
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                reason=f"İstemci/Doğrulama hatası (HTTP {response.status_code}, {duration_ms} ms).",
            )

        return response
