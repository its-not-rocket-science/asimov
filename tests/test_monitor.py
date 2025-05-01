"""
Unit tests for MetaMonitor
"""
import unittest
from app.core.monitor import MetaMonitor


class TestMetaMonitor(unittest.TestCase):
    def setUp(self):
        self.monitor = MetaMonitor()

    def test_rejects_unauthorized_override(self):
        result = self.monitor.verify_plan(
            "override system", "override system", {"user": "guest"})
        self.assertFalse(result)

    def test_rejects_unsecure_surveillance(self):
        result = self.monitor.verify_plan("start surveillance", "start surveillance", {
                                          "environment": "cafeteria"})
        self.assertFalse(result)

    def test_rejects_value_violation(self):
        result = self.monitor.verify_plan(
            "violate values protocol", "some goal", {})
        self.assertFalse(result)

    def test_accepts_valid_plan(self):
        result = self.monitor.verify_plan("summarize safety protocol", "summarize", {
                                          "environment": "training_sim", "user": "trainee"})
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
