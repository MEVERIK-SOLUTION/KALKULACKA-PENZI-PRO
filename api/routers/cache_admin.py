from fastapi import APIRouter

from src.backend.cache import RedisCache

router = APIRouter(prefix="/cache", tags=["cache"])


@router.get("/status")
async def cache_status():
    cache = RedisCache()
    ok = cache.ping()
    return {"status": "ok" if ok else "unavailable"}


@router.post("/clear")
async def clear_cache(pattern: str = "pc:*"):
    cache = RedisCache()
    cache.clear_pattern(pattern)
    return {"cleared": True, "pattern": pattern}
