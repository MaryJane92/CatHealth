"""Измерения веса животного."""

from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Date, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models._mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.animal import Animal


class WeightMeasurement(Base, TimestampMixin):
    """Измерение веса животного (кг)."""

    __tablename__ = "weight_measurements"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    animal_id: Mapped[int] = mapped_column(
        ForeignKey("animals.id", ondelete="CASCADE"), nullable=False, index=True
    )

    measured_at: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    value_kg: Mapped[float] = mapped_column(Float, nullable=False)

    # --- Связи ---
    animal: Mapped["Animal"] = relationship(back_populates="weight_measurements")

    def __repr__(self) -> str:
        return f"<WeightMeasurement animal_id={self.animal_id} {self.value_kg}kg>"
