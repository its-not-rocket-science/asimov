# routes.py
"""
FastAPI Routes
--------------
Defines REST API endpoints for moderating AI behavior using the AbstractAISystem.
Handles user input and returns explainable decisions.
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.core.system import AbstractAISystem

moderate_route = APIRouter()

ai_agent = AbstractAISystem()

class UserQuery(BaseModel):
    """
    Schema for incoming moderation requests.
    """
    input: str
    environment: Optional[str] = "simulated_env"
    user_role: Optional[str] = "test_user"

@moderate_route.post("/moderate")
def moderate(query: UserQuery):
    """
    Handle moderation requests by passing user input through the AI moderation system.

    :param query: JSON input with user query, environment, and role.
    :return: A dictionary containing the AI response.
    """
    result = ai_agent.process_input(query.input, query.environment, query.user_role)
    return {"response": result}
