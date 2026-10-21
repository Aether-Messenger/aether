from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .message import Message


class MimeType(str, Enum):
    JPEG = "image/jpeg"
    PNG = "image/png"
    GIF = "image/gif"
    WEBP = "image/webp"
    MP3 = "audio/mpeg"
    OGG = "audio/ogg"
    MP4 = "video/mp4"
    WEBM = "video/webm"
    PDF = "application/pdf"
    TEXT = "text/plain"
    BINARY = "application/octet-stream"


class MessageAttachment(Base):
    __tablename__ = "message_attachments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message_id: Mapped[int] = mapped_column(ForeignKey("messages.id"), nullable=False)
    storage_key: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[MimeType] = mapped_column(
        SQLEnum(
            MimeType,
            name="mime_type_enum",
            values_callable=lambda types: [mime.value for mime in types],
            validate_strings=True,
            native_enum=True,
        ),
        nullable=False,
    )
    position: Mapped[int] = mapped_column(nullable=False)
    size_bytes: Mapped[int] = mapped_column(nullable=False)

    message: Mapped["Message"] = relationship(back_populates="attachments")
