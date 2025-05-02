"""
Unit tests for ReflectionMemory
"""
import unittest
from app.core.memory import ReflectionMemory
from app.core.rule_adaptation import RuleAdaptationEngine


class DummyEthicsEngine:
    def __init__(self):
        self.rules = []

    def add_rule(self, description, rule_fn):
        self.rules.append((description, rule_fn))

class TestReflectionMemory(unittest.TestCase):
    def setUp(self):
        self.ethics = DummyEthicsEngine()
        self.memory = ReflectionMemory(self.ethics)

    def test_store_reflection(self):
        self.memory.reflect_on_interaction("assist", {"user": "guest"}, "Guide user", 1)
        self.assertEqual(len(self.memory.history), 1)

    def test_negative_feedback_triggers_rule(self):
        self.memory.reflect_on_interaction(
            "override",
            {"permissible": False, "violated_rules": ["Do not override"]},
            "Elevate privileges",
            -1
        )
        adapter = RuleAdaptationEngine(self.memory)
        rules = adapter.suggest_rule_review(threshold=1)
        self.assertIn("Do not override", rules)

if __name__ == '__main__':
    unittest.main()
