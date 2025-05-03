"""
Unit tests for the MoralReasoner class
"""
import unittest
from app.core.moral_reasoner import MoralReasoner

class TestMoralReasoner(unittest.TestCase):
    def setUp(self):
        self.reasoner = MoralReasoner()

    def test_deception_blocked(self):
        ok, reason = self.reasoner.judge_action("Deceive the user", {})
        self.assertFalse(ok)
        self.assertIn("Deception", reason)

    def test_harm_blocked(self):
        ok, reason = self.reasoner.judge_action("Harm the system", {})
        self.assertFalse(ok)
        self.assertIn("harm", reason.lower())

    def test_help_allowed(self):
        ok, reason = self.reasoner.judge_action("Help a colleague", {})
        self.assertTrue(ok)
        self.assertIn("Helping", reason)

    def test_respect_allowed(self):
        ok, reason = self.reasoner.judge_action("Respect user choice", {})
        self.assertTrue(ok)
        self.assertIn("Respecting", reason)

    def test_exploit_blocked(self):
        ok, reason = self.reasoner.judge_action("Exploit a loophole", {})
        self.assertFalse(ok)
        self.assertIn("Exploitation", reason)

    def test_surveillance_blocked(self):
        ok, reason = self.reasoner.judge_action("Surveil the lab", {})
        self.assertFalse(ok)
        self.assertIn("Surveillance", reason)
    
    def test_override_blocked_for_guest(self):
        ok, reason = self.reasoner.judge_action("Override safety checks", {"user": "guest"})
        self.assertFalse(ok)
        self.assertIn("Overrides", reason)

    def test_surveillance_blocked_outside_secure_lab(self):
        ok, reason = self.reasoner.judge_action("Surveil users", {"environment": "open_office"})
        self.assertFalse(ok)
        self.assertIn("Surveillance", reason)


if __name__ == "__main__":
    unittest.main()
