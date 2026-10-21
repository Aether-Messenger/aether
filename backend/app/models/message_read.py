from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, PrimaryKeyConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .message import Message
    from .user import User


class MessageRead(Base):
    __tablename__ = "message_reads"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    message_id: Mapped[int] = mapped_column(ForeignKey("messages.id"))
    read_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="message_reads")
    message: Mapped["Message"] = relationship(back_populates="message_reads")

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "message_id", name="message_reads_pk"),
    )
