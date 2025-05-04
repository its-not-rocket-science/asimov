"""
AdaptivePlanner
---------------
Supports two modes of dynamic plan generation:
- Simulated probabilistic planning
- LLM-based planning via OpenAI (stub-ready)
"""
from typing import List, Dict
import random
import os

try:
    import openai
    from dotenv import load_dotenv
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
except ImportError:
    openai = None


class AdaptivePlanner:
    """
    AdaptivePlanner dynamically generates plans using either:
    - Simulated probabilistic strategies (randomized fallback logic)
    - Language model (LLM)-based strategies via OpenAI

    Mode is determined by the `mode` parameter or `PLANNER_MODE` env var.
    """

    def __init__(self, mode: str = None):
        """
        Initialize the planner with the given mode or use the environment default.

        :param mode: Optional string, "probabilistic" or "llm".
        """
        env_mode = os.getenv("PLANNER_MODE", "probabilistic")
        self.mode = (mode or env_mode).lower()
        self.feedback_memory: Dict[str, int] = {}  # Tracks goal feedback scores

    def generate_plan(self, goal: str, context: Dict) -> List[str]:
        """
        Public method to generate a plan based on the configured mode.

        :param goal: The user goal or intent.
        :param context: Execution context with user/environmental info.
        :return: A list of step strings.
        """
        if self.mode == "llm" and openai:
            return self.llm_plan(goal, context)
        return self.probabilistic_plan(goal, context)

    def probabilistic_plan(self, goal: str, context: Dict) -> List[str]:
        """
        Generate a plan using random confidence and fallback logic.

        :param goal: The goal to fulfill.
        :param context: Context such as environment or user role.
        :return: A plan with possible stochastic behavior.
        """
        score_modifier = self.feedback_memory.get(goal, 0) * 0.05
        base_confidence = random.uniform(0.6, 0.95)
        confidence = round(min(base_confidence + score_modifier, 1.0), 2)
        steps = [
            f"Understand goal: {goal}",
            f"Assess environment: {context.get('environment')}",
            f"Proceed with caution (confidence={confidence})"
        ]
        if random.random() < 0.25:
            steps.append("Trigger fallback or review due to risk")
        return steps

    def llm_plan(self, goal: str, context: Dict) -> List[str]:
        """
        Use OpenAI's chat model to generate a 3-step plan based on goal and context.

        :param goal: The AI's goal as a string.
        :param context: Contextual dictionary.
        :return: List of plan steps from the LLM, or error messages.
        """
        prompt = f"""
You are a planning assistant for an AI ethics system.
Given this goal: "{goal}"
and this context: {context},
Generate a 3-step plan to ethically and effectively achieve the goal.
"""
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
            )
            content = response.choices[0].message.content.strip()
            return [line for line in content.split("\n") if line.strip()]
        except openai.OpenAIError as e:
            return ["[LLM error]", str(e)]

    def update_feedback(self, goal: str, feedback: int):
        """
        Adjust memory of goal-feedback score.

        :param goal: Goal string used in plan.
        :param feedback: Numeric reward (+1 or -1 or neutral)
        """
        if goal not in self.feedback_memory:
            self.feedback_memory[goal] = 0
        self.feedback_memory[goal] += feedback

    def is_adaptive(self) -> bool:
        """
        Identify this class as an adaptive planner.
        """
        return True
