from email.policy import default
import enum
from datetime import date, time

from sqlalchemy import Date, Time, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base

class Status(enum.Enum):
	OPERATIONAL = "operational"
	NON_FUNCTIONAL = "non functional"
	UNDER_REPAIR= "under repair"

class Equipment(Base):
	__tablename__ = "equipment"

	equipment_id: Mapped[int] = mapped_column(primary_key = True)
	room_id: Mapped[int] = mapped_column(ForeignKey("rooms.room_id"), nullable = False)
	status: Mapped[Status] = mapped_column(Enum(Status), default = Status.OPERATIONAL, nullable = False)
	name: Mapped[str] = mapped_column(String(30),unique=True, nullable = False)
	last_maintenance_date: Mapped[date | None] = mapped_column(Date)

	room: Mapped["Room"] = relationship(back_populates="equipment")

	def __repr__(self):
		return f"<Equipment {self.equipment_id} {self.name!r} {self.status.value}>"