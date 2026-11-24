"""Точка входа FastAPI-приложения Cat Health Tracker.

Скелет: middleware, обработчики исключений, заглушки роутеров.
Бизнес-логика будет добавлена на следующих этапах.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Жизненный цикл приложения."""
    # Старт
    yield
    # Завершение


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# CORS для локального frontend (Vite dev server)
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


@app.get("/api/health")
async def health_check():
    """Проверка работоспособности API."""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.VERSION,
    }


# Роутеры будут подключены здесь после реализации:
# from app.routers import animals, studies, metrics, documents, dashboard
# app.include_router(animals.router, prefix="/api/animals", tags=["animals"])
# app.include_router(studies.router, prefix="/api/studies", tags=["studies"])
# app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])
# app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
# app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
