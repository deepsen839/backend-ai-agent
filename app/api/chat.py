from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from db.database import (
    get_db
)

from models.requests import (
    ChatRequest
)

from services.chat_service import (
    ChatService
)

from memory.sqlite_memory import (
    SQLiteMemory
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/{user_id}")
def chat(
    user_id: str,
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    return ChatService.chat(
        db=db,
        user_id=user_id,
        message=request.message
    )


@router.get("/{user_id}/history")
def history(
    user_id: str,
    db: Session = Depends(get_db)
):
    memory = SQLiteMemory(db)

    history = memory.get_history(
        user_id
    )

    return [
        {
            "role": item.role,
            "content": item.content,
            "session_id":
                item.session_id,
            "created_at":
                item.created_at
        }
        for item in history
    ]


@router.delete("/{user_id}/memory")
def delete_memory(
    user_id: str,
    db: Session = Depends(get_db)
):
    memory = SQLiteMemory(db)

    memory.clear_memory(
        user_id
    )

    return {
        "status": "deleted",
        "user_id": user_id
    }