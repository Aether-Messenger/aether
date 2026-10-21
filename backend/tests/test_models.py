import unittest

from sqlalchemy import create_engine, event, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, configure_mappers

from app.models import (
    Base,
    Chat,
    ChatMember,
    ChatMemberRole,
    ChatType,
    Message,
    MessageAttachment,
    MessageContent,
    MessageRead,
    MimeType,
    User,
)


class ModelTests(unittest.TestCase):
    def setUp(self):
        configure_mappers()
        self.engine = create_engine("sqlite://")

        @event.listens_for(self.engine, "connect")
        def enable_foreign_keys(connection, _):
            connection.execute("PRAGMA foreign_keys=ON")

        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)
        self.addCleanup(self.engine.dispose)
        self.addCleanup(self.session.close)
        self.user = User(username="Alice", login="Alice", password_hash="hash")
        self.chat = Chat(type=ChatType.GROUP)
        self.message = Message(chat=self.chat, sender=self.user)
        self.session.add(self.message)
        self.session.flush()

    def test_round_trip_relationships_and_defaults(self):
        self.chat.members.append(ChatMember(user=self.user, role=ChatMemberRole.OWNER))
        self.message.message_content = MessageContent(text="Hello")
        self.message.message_reads.append(MessageRead(user=self.user))
        for position in (1, 0):
            self.message.attachments.append(
                MessageAttachment(
                    storage_key=f"files/{position}",
                    mime_type=MimeType.PNG,
                    position=position,
                    size_bytes=100,
                )
            )
        self.session.commit()
        self.session.expire_all()

        self.assertEqual(self.user.messages, [self.message])
        self.assertEqual(self.chat.members, self.user.chat_memberships)
        self.assertEqual(self.chat.members[0].role, ChatMemberRole.OWNER)
        self.assertIsNotNone(self.chat.members[0].joined_at)
        self.assertIsNotNone(self.message.created_at)
        self.assertIsNone(self.message.deleted_at)
        self.assertIsNone(self.message.message_content.edited_at)
        self.assertEqual(self.message.message_content.message_id, self.message.id)
        self.assertIsNotNone(self.message.message_reads[0].read_at)
        self.assertEqual([a.position for a in self.message.attachments], [0, 1])
        self.assertEqual(self.message.attachments[0].mime_type, MimeType.PNG)

    def test_composite_keys_reject_duplicate_members_and_reads(self):
        for model, values in (
            (
                ChatMember,
                dict(
                    user_id=self.user.id,
                    chat_id=self.chat.id,
                    role=ChatMemberRole.MEMBER,
                ),
            ),
            (MessageRead, dict(user_id=self.user.id, message_id=self.message.id)),
        ):
            with self.subTest(model=model.__name__):
                self.session.execute(model.__table__.insert().values(**values))
                with self.assertRaises(IntegrityError):
                    with self.session.begin_nested():
                        self.session.execute(model.__table__.insert().values(**values))

    def test_content_primary_key_and_foreign_key(self):
        self.message.message_content = MessageContent(text="First")
        self.session.flush()
        with self.assertRaises(IntegrityError):
            with self.session.begin_nested():
                self.session.execute(
                    MessageContent.__table__.insert().values(
                        message_id=self.message.id, text="Duplicate"
                    )
                )
        with self.assertRaises(IntegrityError):
            with self.session.begin_nested():
                self.session.execute(
                    MessageContent.__table__.insert().values(
                        message_id=self.message.id + 1, text="Orphan"
                    )
                )

    def test_chat_deletion_removes_owned_rows(self):
        self.chat.members.append(ChatMember(user=self.user, role=ChatMemberRole.MEMBER))
        self.message.message_content = MessageContent(text="Hello")
        self.message.message_reads.append(MessageRead(user=self.user))
        self.message.attachments.append(
            MessageAttachment(
                storage_key="file", mime_type=MimeType.PDF, position=0, size_bytes=100
            )
        )
        self.session.commit()
        self.session.expire_all()
        self.session.delete(self.chat)
        self.session.commit()

        for model in (
            Chat,
            ChatMember,
            Message,
            MessageContent,
            MessageRead,
            MessageAttachment,
        ):
            self.assertEqual(
                self.session.scalar(select(func.count()).select_from(model)), 0
            )
        self.assertIsNotNone(self.session.get(User, self.user.id))

    def test_login_is_unique_ignoring_case(self):
        with self.assertRaises(IntegrityError):
            with self.session.begin_nested():
                self.session.add(
                    User(username="Other", login="alice", password_hash="hash")
                )
                self.session.flush()


if __name__ == "__main__":
    unittest.main()
