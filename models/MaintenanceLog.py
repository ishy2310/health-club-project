from datetime import date
from typing import Optional

from sqlalchemy import CheckConstraint, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class MaintenanceLog(Base):
    """One reported issue for one piece of equipment, tracked until resolved."""

    __tablename__ = "maintenance_logs"
    __table_args__ = (
        CheckConstraint(
            "status IN ('OPEN', 'IN_PROGRESS', 'RESOLVED')", name="ck_maintenance_status"
        ),
        CheckConstraint(
            "resolved_date IS NULL OR resolved_date >= reported_date",
            name="ck_maintenance_dates",
        ),
    )

    log_id: Mapped[int] = mapped_column(primary_key=True)
    equipment_id: Mapped[int] = mapped_column(
        ForeignKey("equipment.equipment_id", ondelete="CASCADE")
    )
    issue_description: Mapped[str] = mapped_column(Text)
    reported_date: Mapped[date] = mapped_column(server_default=func.current_date())
    status: Mapped[str] = mapped_column(String(20), default="OPEN")
    resolved_date: Mapped[Optional[date]]  # stays NULL until the issue is resolved

    equipment: Mapped["Equipment"] = relationship()

    def __repr__(self):
        return f"<MaintenanceLog {self.log_id} equipment={self.equipment_id} {self.status}>"