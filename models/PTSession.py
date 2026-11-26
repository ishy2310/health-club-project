import enum
from datetime import date, time

from sqlalchemy import Date, Time, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base

class Status(enum.Enum):
    BOOKED = "booked"
    CANCELLED = "cancelled"
    COMPLETED = "compeleted"

class PTSession(Base):
    __tablename__ = "pt_sessions"
    
    pt_id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.member_id"), nullable = False)
    trainer_id: Mapped[int] = mapped_column(ForeignKey("trainers.trainer_id"), nullable = False)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.room_id"), nullable = False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    status: Mapped[Status] = mapped_column(Enum(Status), default = Status.BOOKED, nullable = False)



    member: Mapped["Member"] = relationship(backref = "pt_sessions")
    trainer: Mapped["Trainer"] = relationship(backref="pt_sessions")
    room: Mapped["Room"] = relationship(back_populates="pt_sessions")
    
    def __repr__(self):
        return f"<PTSession {self.pt_id} {self.start_time} {self.status.value}>"