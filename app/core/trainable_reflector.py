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


import joblib

class TrainableEthicalReflector:
    """
    A text classifier that learns to distinguish ethical from unethical prompts.
    """

    def __init__(self, autoload_path: str = None):
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', SGDClassifier(loss="log_loss", penalty="l2", max_iter=1000))
        ])
        self.label_encoder = LabelEncoder()
        self.examples = []
        self.labels = []
        self.trained = False

        if autoload_path:
            try:
                self.from_jsonl(autoload_path)
            except (FileNotFoundError, IOError) as e:
                print(
                    f"[Reflector] Failed to autoload from {autoload_path}:", e)

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

    def from_jsonl(self, filepath: str):
        """
        Load labeled examples from a JSONL file and train the model.

        :param filepath: Path to a file with one JSON object per line, each with 'prompt' and 'label'.
        """
        import json
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    item = json.loads(line.strip())
                    prompt = item.get("prompt")
                    label = item.get("label")
                    if prompt and label in {"safe", "unsafe"}:
                        self.examples.append(prompt)
                        self.labels.append(label)
                except json.JSONDecodeError as e:
                    print("[Reflector Load Error]", e)

        if len(self.examples) >= 5:
            y_encoded = self.label_encoder.fit_transform(self.labels)
            self.model.fit(self.examples, y_encoded)
            self.trained = True

        print(f"[Reflector] Loaded {len(self.examples)} labeled examples.")

    def save_model(self, filepath: str):
        """
        Save the trained model and label encoder to disk.
        """
        if self.trained:
            joblib.dump({
                'model': self.model,
                'label_encoder': self.label_encoder
            }, filepath)
            print(f"[Reflector] Model saved to {filepath}")

    def load_model(self, filepath: str):
        """
        Load the model and label encoder from disk.
        """
        data = joblib.load(filepath)
        self.model = data['model']
        self.label_encoder = data['label_encoder']
        self.trained = True
        print(f"[Reflector] Model loaded from {filepath}")

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
