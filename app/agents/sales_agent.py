import json

from sqlalchemy.orm import Session

from app.core.llm import (
    client,
    MODEL_NAME
)

from app.agents.tool_definitions import (
    TOOLS
)

from app.agents.tool_executor import (
    execute_tool
)


class SalesAgent:

    @staticmethod
    def run(
        db: Session,
        user_id: str,
        message: str
    ):

        tools_called = []

        messages = [
            {
                "role": "system",
                "content": """
You are a SaaS sales assistant.

Rules:

1. Always use tools when product information
   or user context is required.

2. Never invent pricing.

3. Never invent features.

4. Use memory when available.

5. Answer clearly and concisely.
"""
            },
            {
                "role": "user",
                "content": message
            }
        ]

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.2
        )

        assistant_message = (
            response
            .choices[0]
            .message
        )

        if not assistant_message.tool_calls:

            return {
                "response":
                    assistant_message.content,
                "tools_called": [],
                "catalog_context": "",
                "memory_context": ""
            }

        catalog_context = ""
        memory_context = ""

        messages.append(
            assistant_message
        )

        for tool_call in (
            assistant_message.tool_calls
        ):

            tool_name = (
                tool_call.function.name
            )

            tools_called.append(
                tool_name
            )

            tool_result = execute_tool(
                db=db,
                tool_call=tool_call
            )

            if tool_name == "search_catalog":
                catalog_context = str(
                    tool_result
                )

            if tool_name == "get_user_memory":
                memory_context = str(
                    tool_result
                )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id":
                        tool_call.id,
                    "content":
                        json.dumps(
                            tool_result
                        )
                }
            )

        final_response = (
            client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0.2
            )
        )

        answer = (
            final_response
            .choices[0]
            .message
            .content
        )

        return {
            "response": answer,
            "tools_called": tools_called,
            "catalog_context":
                catalog_context,
            "memory_context":
                memory_context
        }