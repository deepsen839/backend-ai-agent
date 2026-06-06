from sqlalchemy.orm import Session

from db.models import Escalation


def flag_for_human(
    db: Session,
    user_id: str,
    reason: str
):
    escalation = Escalation(
        user_id=user_id,
        reason=reason
    )

    db.add(escalation)
    db.commit()

    return {
        "status": "flagged",
        "reason": reason
    }