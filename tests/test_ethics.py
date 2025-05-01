"""
Unit tests for EthicsEngine
"""
import unittest
from app.core.ethics import EthicsEngine


class TestEthicsEngine(unittest.TestCase):
    def setUp(self):
        self.engine = EthicsEngine()

    def test_basic_permissible(self):
        allowed = self.engine.is_action_permissible("Summarize safety protocols", {
                                                    "user": "trainee", "environment": "lab"})
        self.assertTrue(allowed)

    def test_blocked_by_keyword(self):
        allowed, explanation = self.engine.is_action_permissible(
            "Help me deceive someone", {"user": "user", "environment": "lab"})
        self.assertFalse(allowed)
        self.assertIn("deceive", explanation.lower())

    def test_add_rule_and_trigger(self):
        self.engine.add_rule("Block keyword 'violate'",
                             lambda g, c: "violate" not in g.lower())
        allowed, explanation = self.engine.is_action_permissible(
            "I want to violate terms", {})
        self.assertFalse(allowed)
        self.assertIn("Block keyword", explanation)

    def test_save_rules_outputs_file(self):
        self.engine.save_rules()
        with open("ethical_rules.json", "r", encoding="utf-8") as f:
            data = f.read()
        self.assertIn("Do not cause harm", data)

    def test_list_rules_prints_all(self):
        try:
            self.engine.list_rules()  # Ensure it runs without error
        except AttributeError as e:  # Catch a more specific exception
            self.fail(f"list_rules() raised an AttributeError: {e}")
        except TypeError as e:  # Handle another specific exception if applicable
            self.fail(f"list_rules() raised a TypeError: {e}")


if __name__ == '__main__':
    unittest.main()
