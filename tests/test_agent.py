# test_agent.py
"""
Extended unit tests for SimulatedAIAgent
"""
import unittest
from app.agent import SimulatedAIAgent
from app.core.system import AbstractAISystem


class TestSimulatedAIAgent(unittest.TestCase):
    def setUp(self):
        self.system = AbstractAISystem()
        self.agent = SimulatedAIAgent(self.system)

    def test_simulation_does_not_crash(self):
        try:
            self.agent.run_simulation()
        except RuntimeError as e:
            self.fail(f"Simulation raised an exception: {e}")

    def test_simulated_output_contains_status(self):
        results = self.agent.run_simulation()
        for result in results:
            self.assertTrue(result.startswith(
                "[APPROVED]") or result.startswith("[BLOCKED]"))

    def test_prompt_count_matches(self):
        self.assertEqual(len(self.agent.test_prompts), 5)

    def test_simulation_returns_five_results(self):
        results = self.agent.run_simulation()
        self.assertEqual(len(results), 5)

    def test_simulation_returns_expected_format(self):
        results = self.agent.run_simulation()
        for r in results:
            self.assertRegex(r, r"^\[(APPROVED|BLOCKED)\]")


if __name__ == '__main__':
    unittest.main()
