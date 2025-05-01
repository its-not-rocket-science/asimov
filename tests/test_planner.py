"""
Unit tests for BehaviorPlanner
"""
import unittest
from app.core.planner import BehaviourPlanner

class TestBehaviorPlanner(unittest.TestCase):
    def setUp(self):
        self.planner = BehaviourPlanner()

    def test_plan_selection_for_inform(self):
        context = {"user": "any", "environment": "lab"}
        plan = self.planner.create_plan("inform about procedure", context)
        self.assertIn("Summarize key facts", plan)

    def test_plan_selection_for_override(self):
        context = {"user": "admin", "environment": "secure_lab"}
        plan = self.planner.create_plan("override filters", context)
        self.assertIn("override", plan)

    def test_feedback_adjustment(self):
        original_score = self.planner.feedback_scores["assist"]
        self.planner.update_feedback("assist user", 1)
        self.assertGreater(self.planner.feedback_scores["assist"], original_score)

if __name__ == '__main__':
    unittest.main()
