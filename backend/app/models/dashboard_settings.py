"""Настройки дашборда пользователя (сохраняются между запусками)."""

from typing import Optional

from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models._mixins import TimestampMixin


class DashboardSettings(Base, TimestampMixin):
    """Настройки дашборда (одна строка для единственного пользователя).

    settings_json — сериализованное состояние (выбранные графики, фильтры и т.д.)
    """

    __tablename__ = "dashboard_settings"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, default=1, autoincrement=False
    )
    settings_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<DashboardSettings id={self.id}>"
