from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Trainer(Base):
    __tablename__ = "trainers"

    trainer_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20))

    def __repr__(self):
        return f"<Trainer {self.trainer_id} {self.first_name} {self.last_name}>"
    