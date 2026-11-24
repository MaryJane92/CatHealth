"""Настройка SQLAlchemy 2.0 engine и сессий.

Синхронный engine — для Alembic-миграций.
Async engine — для FastAPI runtime.
"""

from collections.abc import AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

from app.config import settings


# ── Синхронный engine (для Alembic и скриптов) ──────────────────────
sync_engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False},  # SQLite + FastAPI
)

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# ── Async engine (для FastAPI runtime) ──────────────────────────────
async_engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False},
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Базовый класс для всех ORM-моделей."""

    pass


# ── Зависимости для FastAPI ──────────────────────────────────────────

def get_db() -> Generator[Session, None, None]:
    """Синхронная сессия БД (для не-async роутеров)."""
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Async-сессия БД (для async роутеров)."""
    async with AsyncSessionLocal() as db:
        yield db
