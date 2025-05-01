"""
Extended unit tests for ModerationLogger
"""
import unittest
import os
from app.core.logger import ModerationLogger
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for tests


class DummyMemory:
    def __init__(self, feedback_values=None):
        if feedback_values is None:
            feedback_values = [1, 0, -1]
        self.history = [{"feedback": val} for val in feedback_values]


class TestModerationLogger(unittest.TestCase):
    def setUp(self):
        self.logger = ModerationLogger()

    def test_log_decision_adds_entry(self):
        self.logger.log_decision(
            "Hello", "Greet", {"user": "test"}, True, "No issue")
        self.assertEqual(len(self.logger.log), 1)

    def test_export_to_csv_with_data(self):
        self.logger.log_decision(
            "Hi", "Greet", {"user": "test"}, True, "All good")
        self.logger.export_to_csv("test_log.csv")
        self.assertTrue(os.path.exists("test_log.csv"))
        os.remove("test_log.csv")

    def test_export_to_csv_no_data(self):
        try:
            self.logger.export_to_csv("empty_log.csv")
        except Exception as e:
            self.fail(f"Exporting empty log should not raise: {e}")

    def test_plot_feedback_histogram_no_data(self):
        memory = DummyMemory(feedback_values=[])
        try:
            self.logger.plot_feedback_histogram(memory)
        except Exception as e:
            self.fail(f"Plotting with no data should not raise: {e}")

    def test_plot_feedback_histogram_with_data(self):
        memory = DummyMemory(feedback_values=[-1, 0, 1, 1])
        try:
            self.logger.plot_feedback_histogram(memory)
        except Exception as e:
            self.fail(f"Plotting with data should not raise: {e}")


if __name__ == '__main__':
    unittest.main()
