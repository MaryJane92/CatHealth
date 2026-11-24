"""Модель животного — центральная сущность."""

from datetime import date, datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String, Date, Boolean, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models._mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.weight_measurement import WeightMeasurement
    from app.models.study import Study
    from app.models.document import Document


class Animal(Base, TimestampMixin):
    """Животное (кошка)."""

    __tablename__ = "animals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # --- Основные данные ---
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    birth_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    sex: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)  # "м" / "ж"
    diagnoses: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Архивный статус (True — в архиве, не показывается по умолчанию)
    is_archived: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    # --- Связи ---
    weight_measurements: Mapped[List["WeightMeasurement"]] = relationship(
        back_populates="animal",
        cascade="all, delete-orphan",
    )
    studies: Mapped[List["Study"]] = relationship(
        back_populates="animal",
        cascade="all, delete-orphan",
    )
    documents: Mapped[List["Document"]] = relationship(
        back_populates="animal",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Animal id={self.id} name={self.name!r}>"
