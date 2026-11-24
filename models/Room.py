import enum

from sqlalchemy import DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .Base import Base

class Type(enum.Enum):
	STUDIO = "studio"
	TRAINING = "training"

class Room(Base):
	__tablename__ = "rooms"

	room_id: Mapped[int]= mapped_column(primary_key=True)
	capacity: Mapped[int] = mapped_column(nullable = False)
	type: Mapped[Type] = mapped_column(Enum(Type), default = Type.STUDIO, nullable = False)
	name: Mapped[str] = mapped_column(String(30),unique=True)

	pt_sessions: Mapped[list["PTSession"]] = relationship(back_populates="room")

	def __repr__(self):
		return f"<Room {self.room_id} {self.name!r}>"