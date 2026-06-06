from sqlalchemy.orm import Session

from agents.evaluator import (
    Evaluator
)

from db.models import (
    EvalLog
)


class EvalService:

    @staticmethod
    def evaluate_and_log(
        db: Session,
        user_id: str,
        session_id: str,
        user_message: str,
        response: str,
        catalog_context: str,
        memory_context: str
    ):
        evaluation = (
            Evaluator.evaluate(
                user_message=user_message,
                response=response,
                catalog_context=
                    catalog_context,
                memory_context=
                    memory_context
            )
        )

        log = EvalLog(
            user_id=user_id,
            session_id=session_id,
            groundedness=
                evaluation[
                    "groundedness"
                ],
            relevance=
                evaluation[
                    "relevance"
                ],
            confidence=
                evaluation[
                    "confidence"
                ],
            flagged=
                evaluation[
                    "flagged"
                ],
            reasoning=
                evaluation[
                    "reasoning"
                ]
        )

        db.add(log)
        db.commit()

        return evaluation