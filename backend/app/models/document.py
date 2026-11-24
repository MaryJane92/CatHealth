"""Документы (загруженные файлы)."""

from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models._mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.animal import Animal
    from app.models.study import Study


class Document(Base, TimestampMixin):
    """Загруженный документ (PDF, изображение и т.д.).

    Может быть связан с исследованием (если распознан),
    либо быть самостоятельным документом животного.
    """

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    animal_id: Mapped[int] = mapped_column(
        ForeignKey("animals.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Дата исследования (для группировки/сортировки)
    study_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    # Тип документа: "Анализ крови", "УЗИ", "Справка" и т.д.
    document_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    # Имя файла в uploads/
    filename: Mapped[str] = mapped_column(String(300), nullable=False)

    # Связь с исследованием (опциональная)
    study_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("studies.id", ondelete="SET NULL"), nullable=True
    )

    # --- Связи ---
    animal: Mapped["Animal"] = relationship(back_populates="documents")
    study: Mapped[Optional["Study"]] = relationship(back_populates="documents")

    def __repr__(self) -> str:
        return f"<Document id={self.id} filename={self.filename!r}>"
