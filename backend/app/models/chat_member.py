from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .chat import Chat
    from .user import User


class ChatMemberRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class ChatMember(Base):
    __tablename__ = "chat_members"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), primary_key=True)
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    role: Mapped[ChatMemberRole] = mapped_column(
        SQLEnum(
            ChatMemberRole,
            name="chat_member_role_enum",
            values_callable=lambda roles: [role.value for role in roles],
            validate_strings=True,
            create_constraint=True,
        ),
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="chat_memberships")
    chat: Mapped["Chat"] = relationship(back_populates="members")
