from email.policy import default
import enum
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Enum, ForeignKey, Numeric, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base

class Status(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class Method(enum.Enum):
    CREDIT = "credit"
    DEBIT = "debit"
    CASH = "cash"

class Payment(Base):
    __tablename__= "payments"
    __table_args__ = (CheckConstraint("amount > 0", name="amount_positive"),)

    payment_id: Mapped[int] = mapped_column(primary_key = True)
    bill_id: Mapped[int] = mapped_column(ForeignKey("bills.bill_id"), nullable = False)
    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.PENDING, nullable=False)
    date: Mapped[Date] = mapped_column(Date, server_default=func.now(), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    method: Mapped[Method] = mapped_column(Enum(Method), nullable = Flase)

    bill: Mapped["Bill"] = relationship(back_populates="payments")

    def __repr__(self):
        return f"<Payment {self.payment_id} bill={self.bill_id} {self.amount} {self.status.value}>"
