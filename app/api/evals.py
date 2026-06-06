from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session
from sqlalchemy import func

from db.database import (
    get_db
)

from db.models import (
    EvalLog
)

router = APIRouter(
    prefix="/chat",
    tags=["Evaluations"]
)


@router.get("/{user_id}/evals")
def get_evals(
    user_id: str,
    db: Session = Depends(get_db)
):
    result = (
        db.query(
            func.avg(
                EvalLog.groundedness
            ),
            func.avg(
                EvalLog.relevance
            ),
            func.avg(
                EvalLog.confidence
            ),
            func.count(
                EvalLog.id
            )
        )
        .filter(
            EvalLog.user_id
            == user_id
        )
        .first()
    )

    return {
        "avg_groundedness":
            result[0] or 0,
        "avg_relevance":
            result[1] or 0,
        "avg_confidence":
            result[2] or 0,
        "responses":
            result[3] or 0
    }