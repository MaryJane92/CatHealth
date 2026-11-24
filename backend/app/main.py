"""Точка входа FastAPI-приложения Cat Health Tracker.

Middleware, обработчики исключений, health-check.
Роутеры подключаются по мере реализации.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Жизненный цикл приложения."""
    # Старт: здесь можно инициализировать соединения, кэши и т.д.
    yield
    # Завершение: закрываем ресурсы
    await app.state.async_engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# Сохраняем ссылку на async engine для disposal при завершении
from app.database import async_engine  # noqa: E402
app.state.async_engine = async_engine


# ── CORS для локального frontend (Vite dev server) ───────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health-check endpoints ───────────────────────────────────────────

@app.get("/api/health")
async def health_check():
    """Проверка работоспособности API."""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.VERSION,
    }


@app.get("/api/health/db")
async def health_check_db():
    """Проверка доступности базы данных."""
    from sqlalchemy import text
    from app.database import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        result = await db.execute(text("SELECT 1"))
        value = result.scalar()
        return {
            "status": "ok" if value == 1 else "error",
            "database": str(settings.DB_PATH),
        }


# ── Роутеры (подключаются по мере реализации) ────────────────────────
# from app.routers import animals, studies, metrics, documents, dashboard, mail
# app.include_router(animals.router, prefix="/api/animals", tags=["animals"])
# app.include_router(studies.router, prefix="/api/studies", tags=["studies"])
# app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])
# app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
# app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
# app.include_router(mail.router, prefix="/api/mail", tags=["mail"])
