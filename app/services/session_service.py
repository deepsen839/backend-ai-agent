from sqlalchemy.orm import Session

from memory.sqlite_memory import (
    SQLiteMemory
)


class SessionService:

    @staticmethod
    def get_or_create_session(
        db: Session,
        user_id: str
    ):
        memory = SQLiteMemory(
            db
        )

        existing = (
            memory.get_latest_session(
                user_id
            )
        )

        if existing:
            return existing.session_id

        return memory.create_session(
            user_id
        )