from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class FitnessGoal(Base):
    __tablename__ = "fitness_goals"
    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'achieved', 'abandoned')", name="ck_goal_status"
        ),
    )

    goal_id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(
        ForeignKey("members.member_id", ondelete="CASCADE")
    )
    goal_type: Mapped[str] = mapped_column(String(50))  # e.g. 'target_weight', 'body_fat'
    target_value: Mapped[Decimal] = mapped_column(Numeric(8, 2))
    status: Mapped[str] = mapped_column(String(20), default="active")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    member: Mapped["Member"] = relationship(back_populates="goals")

    def __repr__(self):
        return f"<FitnessGoal {self.goal_id} {self.goal_type}={self.target_value}>"