import json
import os
from typing import Any, Iterable, Iterator

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional for local execution convenience

    def load_dotenv() -> bool:
        return False


def init_env() -> None:
    """Load local environment variables when a .env file is present."""
    load_dotenv()


def load_env_var(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def safe_str(value: Any) -> str | None:
    if value is None:
        return None
    return str(value).strip()


def normalize_whitespace(value: Any) -> str:
    text = safe_str(value) or ""
    return " ".join(text.split())


def chunked(items: Iterable[Any], size: int) -> Iterator[list[Any]]:
    bucket: list[Any] = []
    for item in items:
        bucket.append(item)
        if len(bucket) >= size:
            yield bucket
            bucket = []
    if bucket:
        yield bucket


def log_event(stage: str, message: str, level: str = "INFO", **context: Any) -> None:
    payload = {"level": level, "stage": stage, "message": message}
    if context:
        payload["context"] = context
    print(json.dumps(payload, ensure_ascii=False))
