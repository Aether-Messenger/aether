from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .message import Message


class MessageContent(Base):
    __tablename__ = "message_content"

    message_id: Mapped[int] = mapped_column(
        ForeignKey("messages.id"), primary_key=True, autoincrement=False
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    edited_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=None, nullable=True
    )

    message: Mapped["Message"] = relationship(back_populates="message_content")
