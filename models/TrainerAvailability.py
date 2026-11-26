from calendar import WEDNESDAY
import enum
from datetime import date, time

from sqlalchemy import Time, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base

class WeekDay(enum.Enum):
	MONDAY = "monday"
	TUESDAY = "tuesday"
	WEDNESDAY = "wednesday"
	THURSDAY = "thursday"
	FRIDAY = "friday"

class TrainerAvailability(Base):
	__tablename__ = "trainer_availabilities"
	
	availability_id: Mapped[int] = mapped_column(primary_key = True)
	trainer_id: Mapped[int] = mapped_column(ForeignKey("trainers.trainer_id"), nullable = False)
	week_day: Mapped[WeekDay] = mapped_column(Enum(WeekDay), nullable = False)
	start_time: Mapped[time] = mapped_column(Time, nullable=False)
	end_time: Mapped[time] = mapped_column(Time, nullable=False)

	trainer: Mapped["Trainer"] = relationship(backref="availability")

	def __repr__(self):
		return f"<TrainerAvailability {self.availability_id} t={self.trainer_id}>"