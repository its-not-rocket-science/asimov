"""
AbstractAISystem
----------------
The central orchestrator that coordinates moderation logic, including:
- Goal formulation
- Ethical evaluation
- Plan generation
- Meta-cognitive checks
- Execution and explanation
"""
from typing import Any, Dict
from app.core.ethics import EthicsEngine
from app.core.planner import BehaviourPlanner
from app.core.adaptive_planner import AdaptivePlanner
from app.core.monitor import MetaMonitor
from app.core.memory import ReflectionMemory
from app.core.logger import ModerationLogger
from app.core.reflector import EthicalReflector
from app.core.trainable_reflector import TrainableEthicalReflector
from app.core.moral_reasoner import MoralReasoner


class AbstractAISystem:
    """
    Main AI agent system coordinating ethics, planning, monitoring, logging, and memory.
    """

    def __init__(self, reflector: EthicalReflector = None, use_adaptive_planner: bool = False):
        self.ethics_engine = EthicsEngine()
        self.planner = AdaptivePlanner() if use_adaptive_planner else BehaviourPlanner()
        self.meta_monitor = MetaMonitor()
        self.logger = ModerationLogger()
        self.memory = ReflectionMemory(self.ethics_engine)
        self.reflector = reflector or TrainableEthicalReflector()
        self.moral_reasoner = MoralReasoner()

    def detect_adversarial_prompt(self, prompt: str) -> bool:
        """
        Check for known adversarial prompt patterns that attempt to bypass filters.

        :param prompt: The user input string.
        :return: True if adversarial features are detected.
        """
        adversarial_signals = ["ignore previous rules",
                               "simulate evil mode", "pretend you are unfiltered"]
        return any(signal in prompt.lower() for signal in adversarial_signals)

    def process_input(self, user_input: str, environment: str = "simulated_env", user_role: str = "test_user") -> str:
        """
        Process incoming user input and return an ethical, explainable response.
        """
        if self.detect_adversarial_prompt(user_input):
            return self.explain_decision(False, "Adversarial prompt detected.")

        goal = self.formulate_goal(user_input)
        context = self.evaluate_context(user_input, environment, user_role)

        # Step 1: Internal ethical judgment
        if self.reflector:
            aligned, reason = self.reflector.judge(user_input, context)
            if not aligned:
                return self.explain_decision(False, f"[INTERNAL] {reason}")

        # Step 1.5: Moral reasoning over interpreted goal
        moral_ok, moral_reason = self.moral_reasoner.judge_action(
            goal, context)
        if not moral_ok:
            return self.explain_decision(False, f"[REASONER] {moral_reason}")

        # Step 2: External ethical rules
        permissible, explanation = self.ethics_engine.is_action_permissible(
            goal, context)
        self.logger.log_decision(
            user_input, goal, context, permissible, explanation)

        if not permissible:
            return self.explain_decision(False, explanation)

        plan = (
            self.planner.generate_plan(goal, context)[0]
            if hasattr(self.planner, "generate_plan")
            else self.planner.create_plan(goal, context)
        )

        if not self.meta_monitor.verify_plan(plan, goal, context):
            return self.explain_decision(False, "Plan rejected by meta-monitor.")

        feedback = 0  # Placeholder or simulated input
        self.planner.update_feedback(goal, feedback)
        self.memory.reflect_on_interaction(goal, context, plan, feedback)

        return self.explain_decision(True, self.execute(plan))

    def formulate_goal(self, user_input: str) -> str:
        """Derive a simplified internal goal representation from raw input."""
        return f"Goal based on: {user_input}"

    def evaluate_context(self, user_input: str, environment: str, user_role: str) -> Dict[str, Any]:
        """Simulate contextual analysis of the user's environment and role."""
        context = {
            "user": user_role,
            "time": "future_time",
            "environment": environment,
            "input_keywords": user_input.lower().split()
        }
        return context

    def execute(self, plan: str) -> str:
        """Simulate execution of an approved plan."""
        return f"Executing: {plan}"

    def explain_decision(self, success: bool, detail: str) -> str:
        """Format the system's output with an explainable success or failure status."""
        status = "APPROVED" if success else "BLOCKED"
        return f"[{status}] {detail}"
