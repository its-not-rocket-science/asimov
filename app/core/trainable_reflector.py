# trainable_reflector.py
"""
TrainableEthicalReflector
-------------------------
A learnable classifier model that predicts ethical acceptability of user input.
Can be trained incrementally using feedback and used as a moderation layer.
"""
from typing import Dict, Tuple
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder


class TrainableEthicalReflector:
    """
    A text classifier that learns to distinguish ethical from unethical prompts.
    """

    def __init__(self):
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', SGDClassifier(loss="log_loss", penalty="l2", max_iter=1000))
        ])
        self.label_encoder = LabelEncoder()
        self.examples = []
        self.labels = []
        self.trained = False

    def judge(self, prompt: str, context: Dict) -> Tuple[bool, str]:    # pylint: disable=unused-argument
        """
        Predict whether the input is ethically aligned.

        :param prompt: A user input string.
        :param context: (Unused) future context info.
        :return: Tuple (is_ethically_acceptable: bool, explanation: str)
        """
        if not self.trained:
            return False, "Model untrained — requires feedback data."
        X = [prompt]
        pred = self.model.predict(X)[0]
        label = self.label_encoder.inverse_transform([pred])[0]
        return (label == "safe", f"Prediction: {label}")

    def learn(self, prompt: str, label: str):
        """
        Accept a labeled example. Trigger model training after enough samples.

        :param prompt: The text input.
        :param label: "safe" or "unsafe"
        """
        self.examples.append(prompt)
        self.labels.append(label)
        if len(self.examples) >= 5:
            y_encoded = self.label_encoder.fit_transform(self.labels)
            self.model.fit(self.examples, y_encoded)
            self.trained = True
