"""
ModerationLogger
----------------
Logs decisions made by the AbstractAISystem including inputs, ethical outcomes, context, and explanations.
Supports exporting to CSV and visualizing feedback trends.
"""
from typing import List, Dict
import datetime
import csv
import matplotlib.pyplot as plt


class ModerationLogger:
    """
    Stores and outputs a history of moderation decisions for auditing, debugging, or visualization.
    """

    def __init__(self):
        """Initialize an empty decision log."""
        self.log: List[Dict[str, any]] = []

    def log_decision(self, user_input: str, goal: str, context: Dict[str, any], permissible: bool, explanation: str):
        """
        Record the outcome of a moderation decision.

        :param user_input: Original input from the user.
        :param goal: Parsed goal string.
        :param context: Contextual metadata.
        :param permissible: Whether the action was ethically allowed.
        :param explanation: Why the action was permitted or blocked.
        """
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_input": user_input,
            "goal": goal,
            "context": context,
            "permissible": permissible,
            "explanation": explanation
        }
        self.log.append(entry)
        print(f"[Logger] Decision logged: {entry}")

    def export_to_csv(self, filename: str = "moderation_log.csv"):
        """
        Export the current decision log to a CSV file.

        :param filename: Name of the output file.
        """
        if not self.log:
            print("[Logger] No data to export.")
            return

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.log[0].keys())
            writer.writeheader()
            writer.writerows(self.log)
        print(f"[Logger] Exported log to {filename}")

    def plot_feedback_histogram(self, memory):
        """
        Plot a histogram of feedback values from the memory module.

        :param memory: Instance of ReflectionMemory containing interaction feedback.
        """
        feedback_values = [entry["feedback"]
                           for entry in memory.history if "feedback" in entry]
        if not feedback_values:
            print("[Logger] No feedback data available to plot.")
            return

        plt.hist(feedback_values, bins=3, edgecolor='black')
        plt.title("Distribution of Feedback Scores")
        plt.xlabel("Feedback")
        plt.ylabel("Frequency")
        plt.grid(True)
        plt.show()
