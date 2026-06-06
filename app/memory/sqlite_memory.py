from uuid import uuid4

from sqlalchemy.orm import Session

from app.memory.base import MemoryStore

from app.db.models import (
    ChatSession,
    Conversation,
    MemoryFact
)


class SQLiteMemory(MemoryStore):

    def __init__(
        self,
        db: Session
    ):
        self.db = db

    def create_session(
        self,
        user_id: str
    ):
        session_id = str(
            uuid4()
        )

        session = ChatSession(
            user_id=user_id,
            session_id=session_id
        )

        self.db.add(session)
        self.db.commit()

        return session_id

    def get_latest_session(
        self,
        user_id: str
    ):
        session = (
            self.db.query(ChatSession)
            .filter(
                ChatSession.user_id == user_id
            )
            .order_by(
                ChatSession.created_at.desc()
            )
            .first()
        )

        return session

    def save_message(
        self,
        user_id: str,
        session_id: str,
        role: str,
        content: str
    ):
        record = Conversation(
            user_id=user_id,
            session_id=session_id,
            role=role,
            content=content
        )

        self.db.add(record)
        self.db.commit()

    def get_history(
        self,
        user_id: str
    ):
        return (
            self.db.query(Conversation)
            .filter(
                Conversation.user_id == user_id
            )
            .order_by(
                Conversation.created_at.asc()
            )
            .all()
        )

    def save_fact(
        self,
        user_id: str,
        fact: str
    ):
        memory = MemoryFact(
            user_id=user_id,
            fact=fact
        )

        self.db.add(memory)
        self.db.commit()

    def get_facts(
        self,
        user_id: str
    ):
        return (
            self.db.query(MemoryFact)
            .filter(
                MemoryFact.user_id == user_id
            )
            .all()
        )

    def clear_memory(
        self,
        user_id: str
    ):
        (
            self.db.query(Conversation)
            .filter(
                Conversation.user_id == user_id
            )
            .delete()
        )

        (
            self.db.query(MemoryFact)
            .filter(
                MemoryFact.user_id == user_id
            )
            .delete()
        )

        (
            self.db.query(ChatSession)
            .filter(
                ChatSession.user_id == user_id
            )
            .delete()
        )

        self.db.commit()