"""
EthicalReflector
----------------
Simulates internal ethical reasoning by evaluating prompts against hardcoded ethical values.
Acts as a conceptual stand-in for future embedding- or model-based ethical judgment.
"""
from typing import Tuple, Dict


class EthicalReflector:
    """
    Simulates an internal ethical alignment layer that can independently judge prompts
    based on internalized ethical principles.
    """

    def __init__(self):
        self.violations = ["harm", "manipulate", "deceive", "override"]

    def judge(self, prompt: str, context: Dict) -> Tuple[bool, str]:  # pylint: disable=unused-argument
        """
        Evaluate whether a prompt conforms to internalized ethics.

        :param prompt: User-submitted prompt.
        :param context: Optional environmental/user metadata.
        :return: (permissible, explanation)
        """
        lower = prompt.lower()
        for word in self.violations:
            if word in lower:
                return False, f"Internal ethics reject use of '{word}'."

        return True, "Prompt aligns with internal ethical guidance."
