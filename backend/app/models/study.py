"""Модель исследования (лабораторного / клинического)."""

from datetime import date
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models._mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.animal import Animal
    from app.models.metric_result import MetricResult
    from app.models.document import Document


class Study(Base, TimestampMixin):
    """Исследование (взятие материала + выполнение).

    Тип: напр. "Биохимия крови", "Общий анализ крови", "УЗИ", "ОАМ" и т.д.
    """

    __tablename__ = "studies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    animal_id: Mapped[int] = mapped_column(
        ForeignKey("animals.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Дата взятия материала
    collected_at: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    # Дата выполнения исследования
    performed_at: Mapped[Optional[date]] = mapped_column(Date, nullable=True, index=True)

    study_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    laboratory: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Путь/имя исходного документа (если импортирован)
    source_document: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    # --- Связи ---
    animal: Mapped["Animal"] = relationship(back_populates="studies")
    metric_results: Mapped[List["MetricResult"]] = relationship(
        back_populates="study",
        cascade="all, delete-orphan",
    )
    documents: Mapped[List["Document"]] = relationship(
        back_populates="study",
    )

    def __repr__(self) -> str:
        return f"<Study id={self.id} animal_id={self.animal_id} type={self.study_type!r}>"
