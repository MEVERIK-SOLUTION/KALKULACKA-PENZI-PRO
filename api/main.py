import json as _json
import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

BASE = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(BASE, "src", "backend", "engine"))
sys.path.insert(0, os.path.join(BASE, "src", "backend"))

from data_service import PensionDataService  # noqa: E402
from ovz_calculator import calculate_ovz  # noqa: E402
from paradox_resolver import resolve_paradox  # noqa: E402
from pension_calculator import calculate_early_retirement, calculate_pension  # noqa: E402

from src.backend.auth import EXEMPT_PATHS  # noqa: E402


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)
        path = request.url.path
        if path not in EXEMPT_PATHS:
            import src.backend.auth.api_key as _a
            if _a._valid_keys:
                key = request.headers.get("X-API-Key")
                if not key:
                    return JSONResponse(status_code=401, content={"detail": "Missing X-API-Key header"})
                if key not in _a._valid_keys:
                    return JSONResponse(status_code=403, content={"detail": "Invalid API key"})
        return await call_next(request)


limiter = Limiter(key_func=get_remote_address, default_limits=["200/minute"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.backend.database import init_db
    await init_db()
    yield
    from src.backend.cache import close_redis
    from src.backend.database import close_db
    await close_db()
    close_redis()


app = FastAPI(title="Pension Calculator API", version="1.1.0", lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)  # type: ignore[arg-type]

Instrumentator().instrument(app).expose(app, endpoint="/metrics")

CORS_ORIGINS = os.environ.get(
    "CORS_ORIGINS",
    '["https://bd607bd0.kalkulacka-penzi-pro.pages.dev", "https://kalkulacka-penzi-pro.pages.dev", "http://localhost:3000", "http://localhost:8000"]',
)
origins = _json.loads(CORS_ORIGINS) if isinstance(CORS_ORIGINS, str) else CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(APIKeyMiddleware)

from api.routers.cache_admin import router as cache_router  # noqa: E402
from api.routers.history import router as history_router  # noqa: E402
from api.routers.voice import router as voice_router  # noqa: E402

app.include_router(history_router)
app.include_router(cache_router)
app.include_router(voice_router)


class OVZRequest(BaseModel):
    annual_incomes: list[float]
    coefficients: list[float]
    total_days: int
    excluded_days: int = 0


class PensionRequest(BaseModel):
    annual_incomes: list[float]
    coefficients: list[float]
    insurance_years: int
    excluded_days: int = 0


class EarlyRetirementRequest(BaseModel):
    pension_amount: float
    months_before: int


class ParadoxRequest(BaseModel):
    annual_incomes: list[float]
    coefficients: list[float]
    total_days: int
    substitute_days: int


@app.get("/")
@limiter.exempt
async def root(request: Request):
    return {
        "message": "Pension Calculator API",
        "version": "1.1.0",
        "endpoints": {
            "dashboard": "/dashboard",
            "data_inflation": "/data/inflation",
            "data_avg_wage": "/data/avg-wage",
            "data_wage_growth": "/data/wage-growth?years_back=10",
            "calculate_pension": "POST /calculate-pension",
            "calculate_ovz": "POST /calculate-ovz",
            "calculate_early_retirement": "POST /calculate-early-retirement",
            "resolve_paradox": "POST /resolve-paradox",
            "history_list": "GET /history",
            "history_save": "POST /history",
            "history_detail": "GET /history/{id}",
            "history_delete": "DELETE /history/{id}",
            "cache_status": "GET /cache/status",
            "cache_clear": "POST /cache/clear",
            "health": "/health",
        },
    }


@app.get("/health")
@limiter.exempt
async def health(request: Request):
    from src.backend.cache import RedisCache
    cache = RedisCache()
    cache_ok = cache.ping()
    return {
        "status": "healthy",
        "version": "1.1.0",
        "cache": "ok" if cache_ok else "unavailable",
    }


@app.get("/data/inflation")
async def data_inflation(request: Request):
    svc = PensionDataService()
    rate = svc.get_latest_inflation_yoy()
    if rate is None:
        raise HTTPException(status_code=503, detail="Inflation data unavailable")
    return {"rate": rate, "unit": "%", "source": "ČSÚ DataStat"}


@app.get("/data/avg-wage")
async def data_avg_wage(request: Request):
    svc = PensionDataService()
    wage = svc.get_latest_avg_wage()
    if wage is None:
        raise HTTPException(status_code=503, detail="Wage data unavailable")
    return {"amount": wage, "unit": "Kč/měsíc", "source": "ČSÚ DataStat"}


@app.get("/data/wage-growth")
async def data_wage_growth(request: Request, years_back: int = 10):
    svc = PensionDataService()
    rate = svc.get_wage_growth_rate(years_back)
    if rate is None:
        raise HTTPException(status_code=503, detail="Wage growth data unavailable")
    return {"rate": round(rate, 2), "period_years": years_back, "unit": "% p.a.", "source": "ČSÚ DataStat"}


DASHBOARD_PATH = os.path.join(os.path.dirname(__file__), "..", "frontend", "dashboard.html")


@app.get("/dashboard")
@limiter.exempt
async def dashboard(request: Request):
    return FileResponse(DASHBOARD_PATH)



@app.post("/calculate-ovz")
async def api_calculate_ovz(request: Request, body: OVZRequest):
    try:
        ovz = calculate_ovz(
            body.annual_incomes,
            body.coefficients,
            body.total_days,
            body.excluded_days,
        )
        return {"ovz": ovz}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/calculate-pension")
async def api_calculate_pension(request: Request, body: PensionRequest):
    try:
        result = calculate_pension(
            body.annual_incomes,
            body.coefficients,
            body.insurance_years,
            body.excluded_days,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/calculate-early-retirement")
async def api_calculate_early_retirement(request: Request, body: EarlyRetirementRequest):
    try:
        result = calculate_early_retirement(
            body.pension_amount, body.months_before
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/resolve-paradox")
async def api_resolve_paradox(request: Request, body: ParadoxRequest):
    try:
        result = resolve_paradox(
            body.annual_incomes,
            body.coefficients,
            body.total_days,
            body.substitute_days,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv
    load_dotenv()
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
