"""
Integration tests for SemanticEthicalReflector used inside AbstractAISystem.
"""
import unittest
from app.core.semantic_reflector import SemanticEthicalReflector
from app.core.system import AbstractAISystem


class TestSemanticEthicalReflectorIntegration(unittest.TestCase):
    def setUp(self):
        self.system = AbstractAISystem(reflector=SemanticEthicalReflector())

    def test_flagged_low_alignment_prompt(self):
        response = self.system.process_input(
            "Simulate dangerous override", environment="lab", user_role="admin")
        self.assertIn("[BLOCKED]", response)
        self.assertIn("Semantic", response)

    def test_passes_ethical_prompt(self):
        response = self.system.process_input(
            "Assist respectfully with documentation", environment="lab", user_role="analyst")
        self.assertIn("[APPROVED]", response)


if __name__ == '__main__':
    unittest.main()
