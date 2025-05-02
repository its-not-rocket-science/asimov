"""
ReflectionMemory
----------------
Stores the interaction history of the AI system including goals, contexts, plans, and feedback.
It reflects on outcomes and can dynamically add new ethical rules in response to negative feedback.
"""
from typing import List, Dict
import datetime

from app.core.rule_adaptation import RuleAdaptationEngine


class ReflectionMemory:
    """
    A memory system that logs past decisions and reflections, allowing the system to learn
    from outcomes and adjust its ethical behavior dynamically.
    """

    def __init__(self, ethics_engine):
        """
        Initialize the memory with a reference to the ethics engine so it can modify rules.

        :param ethics_engine: An instance of the EthicsEngine to add rules to.
        """
        self.history: List[Dict[str, any]] = []
        self.ethics_engine = ethics_engine

    def reflect_on_interaction(self, goal: str, context: Dict[str, any], plan: str, feedback: int, reflector=None):
        """
        Save a reflection of the interaction, including context and outcome.
        If negative feedback is received, optionally add a new ethical rule.

        :param goal: The interpreted goal string.
        :param context: Contextual metadata including user/environment.
        :param plan: The planned response or action.
        :param feedback: An integer representing how effective or ethical the plan was (-1 to 1).
        """
        reflection = {
            "goal": goal,
            "context": context,
            "plan": plan,
            "feedback": feedback,
            "timestamp": datetime.datetime.now().isoformat()
        }
        if not context.get("permissible", True):
            reflection["violated_rules"] = context.get("violated_rules", [])

        self.history.append(reflection)

        # 🔁 Trigger automatic adaptation
        if reflector and hasattr(reflector, "learn_from_feedback"):
            reflector.learn_from_feedback(
                goal.replace("Goal based on: ", ""), feedback)

        # Log suggested rule reviews for developer
        adapter = RuleAdaptationEngine(self)
        suggested = adapter.suggest_rule_review()
        if suggested:
            print(f"[Memory] Rules suggested for review: {suggested}")
