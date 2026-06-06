from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import DateTime

from datetime import datetime

from app.db.database import Base


class ChatSession(Base):
    __tablename__ = "sessions"

    id = Column(
        Integer,
        primary_key=True
    )

    session_id = Column(
        String,
        unique=True,
        index=True
    )

    user_id = Column(
        String,
        index=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(
        Integer,
        primary_key=True
    )

    session_id = Column(
        String,
        index=True
    )

    user_id = Column(
        String,
        index=True
    )

    role = Column(String)

    content = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class MemoryFact(Base):
    __tablename__ = "memory_facts"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        String,
        index=True
    )

    fact = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class EvalLog(Base):
    __tablename__ = "eval_logs"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        String,
        index=True
    )

    session_id = Column(
        String,
        index=True
    )

    groundedness = Column(Float)

    relevance = Column(Float)

    confidence = Column(Float)

    flagged = Column(Boolean)

    reasoning = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Escalation(Base):
    __tablename__ = "escalations"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        String,
        index=True
    )

    reason = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )