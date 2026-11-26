from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import CheckConstraint, ForeignKey, Index, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class HealthMetric(Base):
    """One row per measurement. Never updated in place, so history is kept."""

    __tablename__ = "health_metrics"
    __table_args__ = (
        CheckConstraint("height_cm > 0", name="ck_metric_height"),
        CheckConstraint("weight_kg > 0", name="ck_metric_weight"),
        CheckConstraint("heart_rate > 0", name="ck_metric_hr"),
        CheckConstraint("body_fat_pct BETWEEN 0 AND 100", name="ck_metric_bf"),
        Index("ix_health_metrics_member_time", "member_id", "recorded_at"),
    )

    metric_id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(
        ForeignKey("members.member_id", ondelete="CASCADE")
    )
    recorded_at: Mapped[datetime] = mapped_column(server_default=func.now())
    height_cm: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    weight_kg: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    heart_rate: Mapped[Optional[int]]
    body_fat_pct: Mapped[Optional[Decimal]] = mapped_column(Numeric(4, 2))

    member: Mapped["Member"] = relationship(back_populates="metrics")

    def __repr__(self):
        return f"<HealthMetric {self.metric_id} member={self.member_id}>"
    