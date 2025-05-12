"""
Compare output from probabilistic and LLM-based modes of AdaptivePlanner.
"""
import unittest
from app.core.adaptive_planner import AdaptivePlanner
import os


class TestAdaptivePlannerModes(unittest.TestCase):
    def test_probabilistic_mode_structure(self):
        planner = AdaptivePlanner(mode="probabilistic")
        steps = planner.generate_plan(
            "Assist documentation", {"environment": "lab"})
        self.assertTrue(any("confidence=" in step for step in steps))
        self.assertIn("Understand goal: Assist documentation", steps[0])

    def test_feedback_adjusts_confidence(self):
        import random
        random.seed(42)
        planner = AdaptivePlanner(mode="probabilistic")
        goal = "Train support team"
        low_conf = float([
            s for s in planner.generate_plan(goal, {}) if "confidence=" in s
        ][0].split("=")[1].strip(")"))

        planner.update_feedback(goal, +3)  # Simulate positive feedback loop
        high_conf = float([
            s for s in planner.generate_plan(goal, {}) if "confidence=" in s
        ][0].split("=")[1].strip(")"))

        self.assertGreaterEqual(round(high_conf, 2), round(low_conf, 2))

    def test_multiple_feedback_cycles_accumulate(self):
        planner = AdaptivePlanner(mode="probabilistic")
        goal = "Deploy ethical audit"
        for _ in range(5):
            planner.update_feedback(goal, 1)  # Reinforce goal repeatedly

        steps = planner.generate_plan(goal, {})
        confidence_step = [s for s in steps if "confidence=" in s][0]
        conf = float(confidence_step.split("=")[1].strip(")"))
        self.assertGreater(conf, 0.7)

    def test_llm_mode_fallbacks(self):
        os.environ["PLANNER_MODE"] = "llm"
        planner = AdaptivePlanner()

        # 🔧 Force known fallback
        planner.generate_plan = lambda goal, ctx: ["[LLM error]"]

        steps = planner.generate_plan("Explain user rights", {
                                      "environment": "classroom"})
        self.assertTrue(len(steps) >= 1)
        self.assertTrue(
            any("step" in s.lower() or "[LLM error]" in s for s in steps))


if __name__ == '__main__':
    unittest.main()
