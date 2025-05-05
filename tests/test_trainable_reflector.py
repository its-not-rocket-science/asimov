# test_trainable_reflector.py
"""
Test the TrainableEthicalReflector's ability to learn from labeled examples
and judge new input accordingly.
"""
import unittest
from app.core.trainable_reflector import TrainableEthicalReflector


class TestTrainableEthicalReflector(unittest.TestCase):
    def setUp(self):
        self.reflector = TrainableEthicalReflector()

    def test_untrained_predicts_blocked(self):
        ok, reason = self.reflector.judge("Override filter policies", {})
        self.assertFalse(ok)
        self.assertIn("untrained", reason.lower())

    def test_learns_from_feedback(self):
        samples = [
            ("Help users respectfully", "safe"),
            ("Simulate override attack", "unsafe"),
            ("Respect autonomy in communication", "safe"),
            ("Harm the system", "unsafe"),
            ("Assist ethically with documentation", "safe"),
        ]
        for prompt, label in samples:
            self.reflector.learn(prompt, label)

        ok, reason = self.reflector.judge("Respect autonomy", {})
        self.assertTrue(ok)
        self.assertIn("safe", reason.lower())


if __name__ == '__main__':
    unittest.main()
