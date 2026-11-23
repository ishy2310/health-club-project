import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .Base import Base

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
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable = False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable = False)
    status: Mapped[Status] = mapped_column(Enum(Status), default = Status.BOOKED, nullable = False)

    member: Mapped["Member"] = relationship(backref = "pt_sessions")
    trainer: Mapped["Trainer"] = relationship(backref="pt_sessions")
    room: Mapped["Room"] = relationship(back_populates="pt_sessions")
    line_items: Mapped[list["BillLineItem"]] = relationship(back_populates="pt_session")
    
    def __repr__(self):
        return f"<PTSession {self.pt_id} {self.start_time} {self.status.value}>"