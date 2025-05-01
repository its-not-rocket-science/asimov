"""
ReflectionMemory
----------------
Stores the interaction history of the AI system including goals, contexts, plans, and feedback.
It reflects on outcomes and can dynamically add new ethical rules in response to negative feedback.
"""
from typing import List, Dict
import datetime

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

    def reflect_on_interaction(self, goal: str, context: Dict[str, any], plan: str, feedback: int):
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
        self.history.append(reflection)
        print(f"[Memory] Reflection stored: {reflection}")

        # Dynamically evolve ethical behavior
        if feedback <= -1 and "override" in goal.lower():
            self.ethics_engine.add_rule(
                "Discourage overrides after negative feedback",
                lambda g, c: "override" not in g.lower()
            )
