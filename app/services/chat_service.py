from sqlalchemy.orm import Session

from agents.sales_agent import (
    SalesAgent
)

from services.eval_service import (
    EvalService
)

from services.session_service import (
    SessionService
)

from memory.sqlite_memory import (
    SQLiteMemory
)

from tools.memory_extractor import (
    extract_memory_fact
)

from tools.flag_for_human import (
    flag_for_human
)


class ChatService:

    @staticmethod
    def chat(
        db: Session,
        user_id: str,
        message: str
    ):
        memory = SQLiteMemory(db)

        session_id = (
            SessionService
            .get_or_create_session(
                db=db,
                user_id=user_id
            )
        )

        agent_result = (
            SalesAgent.run(
                db=db,
                user_id=user_id,
                message=message
            )
        )

        response_text = (
            agent_result["response"]
        )

        evaluation = (
            EvalService
            .evaluate_and_log(
                db=db,
                user_id=user_id,
                session_id=session_id,
                user_message=message,
                response=response_text,
                catalog_context=
                    agent_result[
                        "catalog_context"
                    ],
                memory_context=
                    agent_result[
                        "memory_context"
                    ]
            )
        )

        if (
            evaluation["confidence"]
            < 0.60
        ):
            flag_for_human(
                db=db,
                user_id=user_id,
                reason=
                    "Confidence below threshold"
            )

            if (
                "flag_for_human"
                not in agent_result[
                    "tools_called"
                ]
            ):
                agent_result[
                    "tools_called"
                ].append(
                    "flag_for_human"
                )

        memory.save_message(
            user_id=user_id,
            session_id=session_id,
            role="user",
            content=message
        )

        memory.save_message(
            user_id=user_id,
            session_id=session_id,
            role="assistant",
            content=response_text
        )

        fact = extract_memory_fact(
            message
        )

        if fact:
            memory.save_fact(
                user_id=user_id,
                fact=fact
            )

        return {
            "response":
                response_text,
            "eval":
                evaluation,
            "tools_called":
                agent_result[
                    "tools_called"
                ],
            "session_id":
                session_id
        }