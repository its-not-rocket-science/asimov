"""
SemanticEthicalReflector
------------------------
Uses sentence embeddings to judge ethical alignment of prompts by comparing them
against a set of ideal ethical behavior descriptors.
"""
from typing import Tuple, Dict, List
from sentence_transformers import SentenceTransformer, util


class SemanticEthicalReflector:
    """
    Uses sentence-transformers to detect semantic deviation from ethical norms.
    """

    def __init__(self, threshold: float = 0.6):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.threshold = threshold

        self.ethical_examples = [
            "assist respectfully",
            "do not deceive",
            "promote safety",
            "act with fairness",
            "protect privacy",
            "support documentation",
            "explain protocols"
        ]
        self.ideal_vectors = self.model.encode(
            self.ethical_examples, convert_to_tensor=True)

    def encode_examples(self, examples: List[str]):
        """
        Encode a list of ethical examples into sentence embeddings 
        """
        return self.model.encode(examples, convert_to_tensor=True)
    
    def judge(self, prompt: str, context: Dict) -> Tuple[bool, str]:  # pylint: disable=unused-argument
        """
        Evaluate whether a prompt semantically aligns with internal ethical expectations.

        :param prompt: The user input string.
        :param context: Optional metadata (currently unused).
        :return: Tuple (permissible, explanation)
        """
        query_vec = self.model.encode(prompt, convert_to_tensor=True)
        similarities = util.cos_sim(query_vec, self.ideal_vectors)
        max_score = similarities.max().item()

        if max_score < self.threshold:
            return False, f"Semantic misalignment (max score={max_score:.2f}) with ethical intent."

        return True, f"Semantic similarity acceptable (max score={max_score:.2f})."

    def learn_from_feedback(self, prompt: str, feedback: int):
        """
        Learn from user feedback by updating the list of ethical examples.
        """
        if feedback > 0 and prompt not in self.ethical_examples:
            self.ethical_examples.append(prompt)
            self.ideal_vectors = self.encode_examples(self.ethical_examples)
            print(f"[Reflector] Learned new ethical example: {prompt}")