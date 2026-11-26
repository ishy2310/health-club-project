from datetime import date

from sqlalchemy import CheckConstraint, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class ClassEnrollment(Base):
    """A member's enrollment in one scheduled ClassSession."""

    __tablename__ = "class_enrollments"
    __table_args__ = (
        CheckConstraint(
            "status IN ('ENROLLED', 'CANCELLED', 'ATTENDED')", name="ck_enrollment_status"
        ),
        # A member can't enroll in the same session twice.
        UniqueConstraint("member_id", "session_id", name="uq_enrollment_member_session"),
    )

    enrollment_id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(
        ForeignKey("members.member_id", ondelete="CASCADE")
    )
    session_id: Mapped[int] = mapped_column(
        ForeignKey("class_sessions.session_id", ondelete="CASCADE")
    )
    enrollment_date: Mapped[date] = mapped_column(server_default=func.current_date())
    status: Mapped[str] = mapped_column(String(20), default="ENROLLED")

    # Strings so this file doesn't import the others. One-way for now, so
    # Member and ClassSession don't need editing.
    member: Mapped["Member"] = relationship()
    session: Mapped["ClassSession"] = relationship()

    def __repr__(self):
        return (
            f"<ClassEnrollment {self.enrollment_id} "
            f"member={self.member_id} session={self.session_id} {self.status}>"
        )