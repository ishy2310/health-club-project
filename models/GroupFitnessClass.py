import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .Base import Base

class GroupFitnessClass(Base):
	__tablename__ = "fitness_classes"

	class_id: Mapped[int] = mapped_column(primary_key = True)
	name: Mapped[str] = mapped_column(String(30),unique=True, nullable = False)
	description: Mapped[str] = mapped_column(String(300))
	capacity: Mapped[int] = mapped_column(nullable = False)

	def __repr__(self):
		return f"<GroupFitnessClass {self.class_id} {self.class_name!r}>"