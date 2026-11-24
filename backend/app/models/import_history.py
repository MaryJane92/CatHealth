"""История импорта документов (защита от дубликатов)."""

from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models._mixins import TimestampMixin


class ImportHistory(Base, TimestampMixin):
    """Журнал импорта документов — защита от повторного импорта.

    file_hash — хэш содержимого файла (для дедупликации).
    """

    __tablename__ = "import_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    filename: Mapped[str] = mapped_column(String(300), nullable=False)
    file_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    # Путь к файлу в uploads/
    file_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Статус импорта
    status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    # Сообщение об ошибке / детали
    message: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # ID созданного исследования (если импорт успешен)
    study_id: Mapped[Optional[int]] = mapped_column(nullable=True)
    animal_id: Mapped[Optional[int]] = mapped_column(nullable=True)

    # Время импорта (дублирует created_at для явной семантики)
    imported_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<ImportHistory id={self.id} file_hash={self.file_hash[:8]}...>"
