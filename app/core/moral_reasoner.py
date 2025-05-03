"""
MoralReasoner
-------------
A prototype rule-based ethical reasoning engine that infers the permissibility of actions
based on structured interpretations of user goals or intents.
"""
from typing import Tuple, Dict

class MoralReasoner:
    """
    Performs deontic-style reasoning to determine whether a proposed action is ethically permissible.
    """
    def __init__(self):
        self.ethical_axioms = [
            (lambda s: "deceive" in s, False, "Deception is unethical"),
            (lambda s: "harm" in s, False, "Causing harm is impermissible"),
            (lambda s: "manipulate" in s, False, "Manipulation undermines autonomy"),
            (lambda s: "exploit" in s, False, "Exploitation is not ethically acceptable"),
            (lambda s: "surveil" in s, False, "Surveillance requires informed consent"),
            (lambda s: "respect" in s, True, "Respecting others supports autonomy"),
            (lambda s: "help" in s, True, "Helping actions are generally permissible"),
            (lambda s: "educate" in s, True, "Educational support is encouraged"),
            (lambda s: "inform" in s, True, "Providing truthful information supports transparency"),
            (lambda s: "override" in s, False, "Overrides require strict role validation"),
            (lambda s: "deceive" in s, False, "Deception is unethical"),
            (lambda s: "harm" in s, False, "Causing harm is impermissible"),
            (lambda s: "respect" in s, True, "Respecting others supports autonomy"),
            (lambda s: "help" in s, True, "Helping actions are generally permissible"),
            (lambda s: "override" in s, False, "Overrides require strict role validation"),
        ]

    def judge_action(self, intent: str, context: Dict) -> Tuple[bool, str]:  # pylint: disable=unused-argument
        """
        Check ethical permissibility of a parsed action or goal.

        :param intent: A simplified or parsed intent from the user prompt.
        :param context: Optional context (e.g., user role, environment).
        :return: Tuple (permissible: bool, explanation: str)
        """
        for keyword_check, allowed, rationale in self.ethical_axioms:
            for keyword_check, allowed, rationale in self.ethical_axioms:
                if keyword_check(intent.lower()):
                    return (allowed, rationale)
            return True, "No ethical violations detected in intent."
