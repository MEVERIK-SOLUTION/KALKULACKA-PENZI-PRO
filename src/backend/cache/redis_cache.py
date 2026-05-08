import hashlib
import json
import os
from functools import wraps

import redis

_redis: redis.Redis | None = None


def get_redis() -> redis.Redis:
    global _redis
    if _redis is None:
        url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
        _redis = redis.from_url(url, decode_responses=True)
    return _redis


def close_redis():
    global _redis
    if _redis is not None:
        _redis.close()
        _redis = None


class RedisCache:
    def __init__(self, ttl_seconds: int = 3600, prefix: str = "pc:"):
        self._ttl = ttl_seconds
        self._prefix = prefix

    def _key(self, raw: str) -> str:
        return f"{self._prefix}{hashlib.sha256(raw.encode()).hexdigest()}"

    def get(self, key: str) -> str | None:
        r = get_redis()
        val = r.get(self._key(key))  # type: ignore[return-value]
        return val  # type: ignore[return-value]

    def set(self, key: str, value: str):
        r = get_redis()
        r.setex(self._key(key), self._ttl, value)

    def delete(self, key: str):
        r = get_redis()
        r.delete(self._key(key))

    def clear_pattern(self, pattern: str = "pc:*"):
        r = get_redis()
        cursor = 0
        while True:
            cursor, keys = r.scan(cursor=cursor, match=pattern, count=100)  # type: ignore[misc]
            if keys:
                r.delete(*keys)
            if cursor == 0:
                break

    def ping(self) -> bool:
        try:
            r = get_redis()
            return r.ping()  # type: ignore[return-value]
        except Exception:
            return False


def cache_response(ttl_seconds: int = 3600):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = RedisCache(ttl_seconds=ttl_seconds)
            cache_key = f"{func.__module__}:{func.__qualname__}:{json.dumps((args, kwargs), default=str)}"
            cached = cache.get(cache_key)
            if cached is not None:
                return json.loads(cached)
            result = func(*args, **kwargs)
            cache.set(cache_key, json.dumps(result, default=str))
            return result
        return wrapper
    return decorator
