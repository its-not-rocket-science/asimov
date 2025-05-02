"""
RuleAdaptationEngine
--------------------
Scans feedback in ReflectionMemory to identify underperforming ethical rules.
Flags rules that are frequently associated with negative user feedback.
"""
from typing import List, Tuple
from collections import Counter


class RuleAdaptationEngine:
    """
    Analyzes reflection memory to identify ethical rules frequently associated with negative feedback.
    Suggests rules for review based on configurable thresholds.
    """
    def __init__(self, memory):
        self.memory = memory

    def analyze_feedback(self) -> List[Tuple[str, int]]:
        """
        Analyze all interactions with negative feedback and count violations of ethical rules.

        :return: A list of (rule description, violation count) tuples sorted by frequency.
        """
        rule_counter = Counter()
        for entry in self.memory.history:
            if entry["feedback"] < 0 and "violated_rules" in entry:
                for rule in entry["violated_rules"]:
                    rule_counter[rule] += 1
        return rule_counter.most_common()

    def suggest_rule_review(self, threshold: int = 3) -> List[str]:
        """
        Suggest ethical rules that should be reviewed based on repeated association with negative feedback.

        :param threshold: Minimum number of violations required to flag a rule for review.
        :return: A list of rule descriptions.
        """
        stats = self.analyze_feedback()
        return [rule for rule, count in stats if count >= threshold]
