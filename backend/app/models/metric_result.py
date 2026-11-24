"""Результаты показателей по исследованию."""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models._mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.study import Study
    from app.models.metric import Metric


class MetricResult(Base, TimestampMixin):
    """Результат отдельного показателя в исследовании.

    value         — распознанное числовое значение (для графиков)
    raw_value     — исходное строковое значение из документа
    unit          — единица измерения результата
    ref_low       — нижняя граница нормы
    ref_high      — верхняя граница нормы
    """

    __tablename__ = "metric_results"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    study_id: Mapped[int] = mapped_column(
        ForeignKey("studies.id", ondelete="CASCADE"), nullable=False, index=True
    )
    metric_id: Mapped[int] = mapped_column(
        ForeignKey("metrics.id", ondelete="RESTRICT"), nullable=False, index=True
    )

    value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    unit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    ref_low: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ref_high: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    raw_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # --- Связи ---
    study: Mapped["Study"] = relationship(back_populates="metric_results")
    metric: Mapped["Metric"] = relationship(back_populates="results")

    def __repr__(self) -> str:
        return f"<MetricResult study_id={self.study_id} metric_id={self.metric_id} value={self.value}>"
