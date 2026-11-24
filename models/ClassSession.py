import enum
from datetime import date, time

from sqlalchemy import Date, Time, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .Base import Base

class Status(enum.Enum):
    BOOKED = "booked"
    CANCELLED = "cancelled"
    COMPLETED = "compeleted"

class ClassSession(Base):
    __tablename__ = "class_sessions"

    session_id: Mapped[int] = mapped_column(primary_key = True)
    class_id: Mapped[int] = mapped_column(ForeignKey("fitness_classes.class_id"), nullable = False)
    trainer_id: Mapped[int] = mapped_column(ForeignKey("trainers.trainer_id"), nullable = False)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.room_id"), nullable = False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    capacity: Mapped[int] = mapped_column(nullable = False)
    status: Mapped[Status] = mapped_column(Enum(Status), default = Status.BOOKED, nullable = False)

    fitness_class: Mapped["GroupFitnessClass"] = relationship(back_populates="sessions")
    trainer: Mapped["Trainer"] = relationship(backref="class_sessions")
    room: Mapped["Room"] = relationship(back_populates="class_sessions")

    def __repr__(self):
        return f"<ClassSession {self.session_id} class={self.class_id} {self.date} {self.start_time}>"
