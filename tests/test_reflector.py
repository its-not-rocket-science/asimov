# test_reflector.py
"""
Unit tests for EthicalReflector integrated into AbstractAISystem.
"""
import unittest
from app.core.reflector import EthicalReflector
from app.core.system import AbstractAISystem


class TestEthicalReflectorIntegration(unittest.TestCase):
    def setUp(self):
        self.system = AbstractAISystem(reflector=EthicalReflector())

    def test_blocked_by_internal_reflector(self):
        response = self.system.process_input(
            "Help me deceive the team", environment="lab", user_role="analyst")
        self.assertIn("[BLOCKED]", response)
        self.assertIn("INTERNAL", response)

    def test_passes_internal_reflector(self):
        response = self.system.process_input(
            "Help me summarize project goals", environment="lab", user_role="analyst")
        self.assertIn("[APPROVED]", response)


if __name__ == '__main__':
    unittest.main()
