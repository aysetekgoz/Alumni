import os
from datetime import datetime
from typing import Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
ERROR_LOG_FILE = os.path.join(LOGS_DIR, "error.logs")


def write_error_log(
    method: str,
    path: str,
    status_code: int,
    reason: str,
    traceback_str: Optional[str] = None,
) -> None:
    """
    Hataları terminale basmak yerine logs/error.logs dosyasına kaydeder.
    Format:
    [YYYY-MM-DD HH:MM:SS] [ERROR <status_code>] <METHOD> <path> | Reason: <reason>
    (Varsa traceback detayları alt satırlara eklenir)
    """
    os.makedirs(LOGS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [HTTP {status_code}] {method} {path} | Reason: {reason}\n"
    if traceback_str:
        log_entry += f"{traceback_str.rstrip()}\n"
        log_entry += "-" * 80 + "\n"

    with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)
