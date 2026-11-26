from datetime import date
from typing import List, Optional

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class Member(Base):
    __tablename__ = "members"

    member_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    date_of_birth: Mapped[date]
    gender: Mapped[Optional[str]] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    join_date: Mapped[date] = mapped_column(server_default=func.current_date())

    # Related classes live in their own files; strings avoid circular imports.
    goals: Mapped[List["FitnessGoal"]] = relationship(
        back_populates="member", cascade="all, delete-orphan"
    )
    metrics: Mapped[List["HealthMetric"]] = relationship(
        back_populates="member", cascade="all, delete-orphan"
    )

    bills: Mapped[list["Bill"]] = relationship(back_populates="member")

    def __repr__(self):
        return f"<Member {self.member_id} {self.first_name} {self.last_name}>"