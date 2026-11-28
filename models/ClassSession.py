import enum
from datetime import date, time

from sqlalchemy import Date, Time, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base

class CapacityStatus(enum.Enum):
    FULL = "full"
    CANCELLED = "cancelled"
    OPEN = "open"

class ClassSession(Base):
    __tablename__ = "class_sessions"

    session_id: Mapped[int] = mapped_column(primary_key = True)
    class_id: Mapped[int] = mapped_column(ForeignKey("fitness_classes.class_id"), nullable = False)
    trainer_id: Mapped[int] = mapped_column(ForeignKey("trainers.trainer_id"), nullable = True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.room_id"), nullable = True)
    date: Mapped[date] = mapped_column(Date, nullable=True)
    start_time: Mapped[time] = mapped_column(Time, nullable=True)
    end_time: Mapped[time] = mapped_column(Time, nullable=True)
    capacity: Mapped[int] = mapped_column(nullable = False)
    class_session_status: Mapped[CapacityStatus] = mapped_column(Enum(CapacityStatus), default = CapacityStatus.OPEN, nullable = False)

    fitness_class: Mapped["GroupFitnessClass"] = relationship(back_populates="sessions")
    trainer: Mapped["Trainer"] = relationship(backref="class_sessions")
    room: Mapped["Room"] = relationship(back_populates="class_sessions")

    def __repr__(self):
        return f"<ClassSession {self.session_id} class={self.class_id} {self.date} {self.start_time}>"
