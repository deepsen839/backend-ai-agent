import json

from core.llm import (
    client,
    MODEL_NAME
)


class Evaluator:

    @staticmethod
    def evaluate(
        user_message: str,
        response: str,
        catalog_context: str,
        memory_context: str
    ):
        prompt = f"""
Evaluate the assistant response.

User Message:
{user_message}

Assistant Response:
{response}

Catalog Context:
{catalog_context}

Memory Context:
{memory_context}

Return ONLY valid JSON.

Required schema:

{{
    "groundedness": float,
    "relevance": float,
    "confidence": float,
    "flagged": boolean,
    "reasoning": string
}}
"""

        result = (
            client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0,
                response_format={
                    "type": "json_object"
                }
            )
        )

        content = (
            result
            .choices[0]
            .message
            .content
        )

        try:
            return json.loads(
                content
            )

        except Exception:

            return {
                "groundedness": 0.5,
                "relevance": 0.5,
                "confidence": 0.5,
                "flagged": True,
                "reasoning":
                    "Evaluation parsing failed."
            }