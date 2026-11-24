"""Справочник показателей."""

from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models._mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.metric_result import MetricResult


class Metric(Base, TimestampMixin):
    """Справочник лабораторных показателей.

    Хранит название, синонимы (для сопоставления при импорте),
    категорию, единицу измерения и альтернативные единицы.
    """

    __tablename__ = "metrics"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    # Синонимы через разделитель (запятая / перевод строки)
    synonyms: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # Категория: напр. "Биохимия", "Общий анализ крови", "ОАМ"
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    # Основная единица измерения
    unit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    # Альтернативные единицы (для пересчёта)
    alternative_units: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # --- Связи ---
    results: Mapped[List["MetricResult"]] = relationship(
        back_populates="metric",
    )

    def __repr__(self) -> str:
        return f"<Metric id={self.id} name={self.name!r}>"
