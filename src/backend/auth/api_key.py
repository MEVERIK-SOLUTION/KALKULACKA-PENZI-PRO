import os

from fastapi import HTTPException, Request
from fastapi.security import APIKeyHeader

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

API_KEYS_ENV = os.environ.get("API_KEYS", "")
SINGLE_KEY = os.environ.get("API_KEY", "")

_valid_keys: set[str] = set()
if API_KEYS_ENV:
    _valid_keys.update(k.strip() for k in API_KEYS_ENV.split(",") if k.strip())
if SINGLE_KEY:
    _valid_keys.add(SINGLE_KEY)

EXEMPT_PATHS = {"/", "/docs", "/openapi.json", "/redoc", "/dashboard", "/health", "/metrics"}


def is_valid_key(key: str | None) -> bool:
    if not _valid_keys:
        return True
    return key in _valid_keys


async def verify_api_key(request: Request, api_key: str | None = None):
    if request.url.path in EXEMPT_PATHS:
        return True
    if not _valid_keys:
        return True
    key = api_key or request.headers.get("X-API-Key")
    if not key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")
    if not is_valid_key(key):
        raise HTTPException(status_code=403, detail="Invalid API key")
    return True


async def optional_api_key(request: Request) -> str | None:
    return request.headers.get("X-API-Key")
