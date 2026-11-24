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
    DATABASE_URL: str = ""

    # --- Файлы ---
    UPLOADS_DIR: Path = PROJECT_ROOT / "uploads"
    DATA_DIR: Path = PROJECT_ROOT / "data"

    # --- OCR ---
    TESSERACT_CMD: str = ""  # путь к tesseract.exe, если не в PATH

    def model_post_init(self, __context) -> None:  # type: ignore[override]
        # Динамически формируем DATABASE_URL, если не задан явно
        if not self.DATABASE_URL:
            self.DATABASE_URL = f"sqlite:///{self.DB_PATH.as_posix()}"

        # Гарантируем существование каталогов
        self.UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.DB_PATH.parent.mkdir(parents=True, exist_ok=True)


settings = Settings()
