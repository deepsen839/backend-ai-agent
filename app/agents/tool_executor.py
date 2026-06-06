import json

from sqlalchemy.orm import Session

from app.tools.search_catalog import (
    search_catalog
)

from app.tools.get_user_memory import (
    get_user_memory
)


def execute_tool(
    db: Session,
    tool_call
):
    function_name = (
        tool_call.function.name
    )

    arguments = json.loads(
        tool_call.function.arguments
    )

    if function_name == "search_catalog":

        return search_catalog(
            arguments["query"]
        )

    if function_name == "get_user_memory":

        return get_user_memory(
            db=db,
            user_id=arguments["user_id"]
        )

    raise ValueError(
        f"Unknown tool: {function_name}"
    )