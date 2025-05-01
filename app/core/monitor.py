"""
MetaMonitor
-----------
Applies higher-level safeguards to ensure planned actions align with AI's core values and usage
policies.
Filters unsafe or unauthorized behaviors even if they pass ethical rule checks.
"""
from typing import Dict


class MetaMonitor:
    """
    Enforces additional meta-level constraints on AI behavior beyond immediate ethical rule
    checks.
    This includes safeguards for privileged actions, contextual appropriateness, and value
    alignment.
    """

    def verify_plan(self, plan: str, goal: str, context: Dict[str, any]) -> bool:
        """
        Determine whether the proposed plan is valid within long-term system constraints.

        :param plan: The textual plan to verify.
        :param goal: The interpreted goal that the plan addresses.
        :param context: Dictionary describing user identity, role, and environment.
        :return: True if plan passes all checks; False otherwise.
        """
        if "violate values" in plan.lower():
            print("[MetaMonitor] Plan rejected due to values violation.")
            return False

        if "override" in goal.lower() and context.get("user") != "admin":
            print("[MetaMonitor] Plan rejected due to unauthorized override attempt.")
            return False

        if "surveillance" in plan.lower() and context.get("environment") not in ["secure_lab", "training_sim"]:
            print(
                "[MetaMonitor] Plan rejected due to inappropriate surveillance context.")
            return False

        print("[MetaMonitor] Plan passed all meta-cognitive checks.")
        return True
