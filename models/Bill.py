from email.policy import default
import enum
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Enum, ForeignKey, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base

class Status(enum.Enum):
	PAID = "paid"
	PENDING  = "pending"
	CANCELLED = "cancelled"


class Bill(Base):
	__tablename__ = "bills"

	__table_args__ = (CheckConstraint("total >= 0", name="total_not_negative"),)

	bill_id: Mapped[int] = mapped_column(primary_key = True)
	member_id: Mapped[int] = mapped_column(ForeignKey("members.member_id"), nullable = True)
	status: Mapped[Status] = mapped_column(Enum(Status),default = Status.PENDING, nullable = False)
	total: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0, nullable=False)
	date: Mapped[Date] = mapped_column(Date, nullable = False)

	payments: Mapped[list["Payment"]] = relationship(back_populates="bill")
	
	member: Mapped["Member"] = relationship(back_populates="bills")


	def __repr__(self):
		return f"<Bill {self.bill_id} m={self.member_id} {self.total_amount} {self.status.value}>"
