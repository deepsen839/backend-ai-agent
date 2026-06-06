from sqlalchemy.orm import Session

from memory.sqlite_memory import (
    SQLiteMemory
)


def get_user_memory(
    db: Session,
    user_id: str
):
    memory_store = SQLiteMemory(db)

    facts = memory_store.get_facts(
        user_id
    )

    return [
        fact.fact
        for fact in facts
    ]