"""
FastAPI Routes
--------------
Defines REST API endpoints for moderating AI behavior using the AbstractAISystem.
Handles user input and returns explainable decisions.
"""
from typing import Optional
from enum import Enum
from fastapi import APIRouter, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse

moderate_route = APIRouter()

# ai_agent = AbstractAISystem()  # Deprecated: use request.app.state.ai


class UserQuery(BaseModel):
    """
    Schema for incoming moderation requests.
    """
    input: str
    environment: Optional[str] = "simulated_env"
    user_role: Optional[str] = "test_user"


class LabelEnum(str, Enum):
    safe = "safe"
    unsafe = "unsafe"


class FeedbackExample(BaseModel):
    """
    Schema for labeled feedback data.
    """
    prompt: str
    label: LabelEnum


@moderate_route.post("/moderate")
def moderate(query: UserQuery, request: Request):
    """
    Handle moderation requests by passing user input through the AI moderation system.

    :param query: JSON input with user query, environment, and role.
    :return: A dictionary containing the AI response.
    """
    ai_agent = request.app.state.ai
    result = ai_agent.process_input(
        query.input, query.environment, query.user_role)
    return {"response": result}


@moderate_route.post("/feedback")
def submit_feedback(feedback: FeedbackExample, request: Request):
    """
    Accept feedback data to improve the TrainableEthicalReflector.
    """
    reflector = getattr(request.app.state.ai, "reflector", None)
    if reflector and hasattr(reflector, "learn"):
        reflector.learn(feedback.prompt, feedback.label)
        import json
        from pathlib import Path
        labels_file = Path("tools/cli/labels.jsonl")
        labels_file.parent.mkdir(parents=True, exist_ok=True)
        with open(labels_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(
                {"prompt": feedback.prompt, "label": feedback.label}) + "\n")
        return JSONResponse(status_code=200, content={"status": "Feedback recorded"})

    return JSONResponse(status_code=400, content={"error": "Reflector not available"})
