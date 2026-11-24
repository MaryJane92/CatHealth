"""Конфигурация приложения Cat Health Tracker."""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


# Корень проекта: backend/../ = рабочая директория
PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    """Глобальные настройки приложения."""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Основные ---
    APP_NAME: str = "Cat Health Tracker"
    VERSION: str = "0.1.0"
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # --- База данных ---
    DB_PATH: Path = PROJECT_ROOT / "data" / "cat_health.db"
    DATABASE_URL: str = ""        # синхронный URL (для Alembic)
    ASYNC_DATABASE_URL: str = ""  # async URL (для FastAPI runtime)

    # --- Файлы ---
    UPLOADS_DIR: Path = PROJECT_ROOT / "uploads"
    DATA_DIR: Path = PROJECT_ROOT / "data"

    # --- OCR ---
    TESSERACT_CMD: str = ""  # путь к tesseract.exe, если не в PATH

    # --- Яндекс Почта (IMAP + OAuth2) ---
    YANDEX_EMAIL: str = ""
    YANDEX_CLIENT_ID: str = ""
    YANDEX_CLIENT_SECRET: str = ""
    YANDEX_REFRESH_TOKEN: str = ""
    YANDEX_IMAP_HOST: str = "imap.yandex.ru"
    YANDEX_IMAP_PORT: int = 993

    def model_post_init(self, __context) -> None:  # type: ignore[override]
        # Формируем URLs, если не заданы явно
        db_path_posix = self.DB_PATH.as_posix()
        if not self.DATABASE_URL:
            self.DATABASE_URL = f"sqlite:///{db_path_posix}"
        if not self.ASYNC_DATABASE_URL:
            self.ASYNC_DATABASE_URL = f"sqlite+aiosqlite:///{db_path_posix}"

        # Гарантируем существование каталогов
        self.UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    @property
    def mail_configured(self) -> bool:
        """Проверка, настроена ли интеграция с Яндекс Почтой."""
        return bool(self.YANDEX_EMAIL and self.YANDEX_REFRESH_TOKEN)


settings = Settings()
