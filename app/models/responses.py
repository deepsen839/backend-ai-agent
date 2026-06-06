from pydantic import BaseModel
from typing import List


class EvalResult(BaseModel):
    groundedness: float
    relevance: float
    confidence: float
    flagged: bool
    reasoning: str


class ChatResponse(BaseModel):
    response: str
    eval: EvalResult
    tools_called: List[str]
    session_id: str