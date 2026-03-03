from sqlalchemy import String, DateTime, func, JSON
from sqlalchemy.orm import Mapped, mapped_column
from apps.control_plane.app.db.base import Base

class RunHistory(Base):
    __tablename__ = "run_history"

    id: Mapped[int] = mapped_column(primary_key=True)

    bot_name: Mapped[str] = mapped_column(String(100), index=True)
    run_type: Mapped[str] = mapped_column(String(50))  # e.g. "reminder_scan", "weekly_digest"
    status: Mapped[str] = mapped_column(String(20))    # "success" | "failed"

    started_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    meta: Mapped[dict] = mapped_column(JSON, default=dict)  # errors, counts, etc.