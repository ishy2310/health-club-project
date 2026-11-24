from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base

class GroupFitnessClass(Base):
	__tablename__ = "fitness_classes"

	class_id: Mapped[int] = mapped_column(primary_key = True)
	name: Mapped[str] = mapped_column(String(30),unique=True, nullable = False)
	description: Mapped[str] = mapped_column(String(300))
	capacity: Mapped[int] = mapped_column(nullable = False)

	sessions: Mapped[list["ClassSession"]] = relationship(
        back_populates="fitness_class", cascade="all, delete-orphan"
    )

	def __repr__(self):
		return f"<GroupFitnessClass {self.class_id} {self.class_name!r}>"