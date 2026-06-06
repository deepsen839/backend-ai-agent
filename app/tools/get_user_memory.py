from sqlalchemy.orm import Session

from app.memory.sqlite_memory import (
    SQLiteMemory
)


def get_user_memory(
    db: Session,
    user_id: str
):
    memory = SQLiteMemory(db)

    facts = memory.get_facts(
        user_id
    )

    return [
        fact.fact
        for fact in facts
    ]