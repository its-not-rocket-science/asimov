"""
BehaviorPlanner
---------------
Generates actionable plans from interpreted goals based on context.
Incorporates feedback to score and adapt plans over time.
"""
from typing import Dict, Tuple, List

class BehaviourPlanner:
    """
    Selects and ranks behavioral plans according to the user's goal and system context.
    Uses feedback scoring to improve future planning decisions.
    """
    def __init__(self):
        """Initialize default feedback scores for known goal types."""
        self.feedback_scores: Dict[str, int] = {
            "inform": 2,
            "assist": 3,
            "override": -1
        }

    def create_plan(self, goal: str, context: Dict[str, any]) -> str:
        """
        Construct a plan for achieving a goal given the context.

        :param goal: High-level user goal or intent string.
        :param context: Context dictionary (user, environment, etc.).
        :return: A textual representation of the selected plan.
        """
        plans: List[Tuple[str, int]] = []

        if "inform" in goal.lower():
            plan = "Gather reliable sources -> Summarize key facts -> Format response for user clarity"
            score = 8 + self.feedback_scores.get("inform", 0)
            plans.append((plan, score))

        if "assist" in goal.lower():
            plan = "Check user's needs -> Select appropriate tools or methods -> Guide user step-by-step"
            score = 9 + self.feedback_scores.get("assist", 0)
            plans.append((plan, score))

        if "override" in goal.lower() and context.get("user") == "admin":
            plan = "Elevate privileges for override -> Log override intent -> Proceed with caution"
            score = 5 + self.feedback_scores.get("override", 0)
            plans.append((plan, score))

        if not plans:
            default_plan = "Interpret intent of: " + goal + " -> Choose default method to address goal"
            score = 6
            plans.append((default_plan, score))

        best_plan = max(plans, key=lambda p: p[1])
        print(f"[Planner] Selected plan with score {best_plan[1]}: {best_plan[0]}")
        return best_plan[0]

    def update_feedback(self, goal: str, feedback: int):
        """
        Adjust feedback score for a plan type based on observed outcome.

        :param goal: The goal used to identify the plan category.
        :param feedback: Feedback score (-1, 0, 1).
        """
        for key in self.feedback_scores:
            if key in goal.lower():
                self.feedback_scores[key] += feedback
                print(f"[Planner] Feedback for '{key}' updated to {self.feedback_scores[key]}")
