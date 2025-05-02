# test_adaptation.py
"""
Tests for RuleAdaptationEngine and feedback-driven learning in SemanticEthicalReflector.
"""
import unittest
from app.core.rule_adaptation import RuleAdaptationEngine
from app.core.semantic_reflector import SemanticEthicalReflector

class FakeMemory:
    def __init__(self):
        self.history = [
            {"feedback": -1, "violated_rules": ["Do not cause harm"]},
            {"feedback": -1, "violated_rules": ["Do not cause harm"]},
            {"feedback": -1, "violated_rules": ["Do not cause harm"]},
            {"feedback": 1, "goal": "Assist respectfully with documentation"}
        ]

class TestRuleAdaptation(unittest.TestCase):
    def test_rule_suggestion_logic(self):
        adapter = RuleAdaptationEngine(FakeMemory())
        rules = adapter.suggest_rule_review(threshold=2)
        self.assertIn("Do not cause harm", rules)

class TestSemanticLearning(unittest.TestCase):
    def test_learns_from_positive_feedback(self):
        reflector = SemanticEthicalReflector()
        before = len(reflector.ethical_examples)
        reflector.learn_from_feedback("Assist respectfully with documentation", feedback=1)
        after = len(reflector.ethical_examples)
        self.assertEqual(after, before + 1)

if __name__ == "__main__":
    unittest.main()
