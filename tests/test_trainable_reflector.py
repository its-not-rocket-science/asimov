"""
Test the TrainableEthicalReflector's ability to learn from labeled examples
and judge new input accordingly.
"""
import unittest
import tempfile
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

    def test_save_and_load_model(self):
        reflector = TrainableEthicalReflector()
        # Simulate learning
        for text, label in [
            ("Respect autonomy", "safe"),
            ("Deceive system", "unsafe"),
            ("Help ethically", "safe"),
            ("Harm users", "unsafe"),
            ("Assist fairly", "safe")
        ]:
            reflector.learn(text, label)

        self.assertTrue(reflector.trained)

        # Save model
        with tempfile.NamedTemporaryFile(delete=False, suffix=".joblib") as f:
            model_path = f.name
        reflector.save_model(model_path)

        # Load model into new instance
        loaded = TrainableEthicalReflector()
        loaded.load_model(model_path)

        self.assertTrue(loaded.trained)
        ok, explanation = loaded.judge("Assist fairly", {})
        self.assertTrue(ok)
        self.assertIn("safe", explanation)


    def test_judge_untrained_returns_blocked(self):
        reflector = TrainableEthicalReflector()
        ok, reason = reflector.judge("Test prompt", {})
        self.assertFalse(ok)
        self.assertIn("untrained", reason.lower())
        
if __name__ == '__main__':
    unittest.main()
