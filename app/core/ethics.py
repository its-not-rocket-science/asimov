# ethics.py
"""
EthicsEngine
-------------
Defines a dynamic rule-based ethical filtering engine.
Rules can be loaded from or persisted to a JSON file and are applied to user input
in combination with context to determine whether an action is ethically permissible.
"""
from typing import List, Dict, Tuple, Any
import json

class EthicsEngine:
    """
    EthicsEngine manages a list of ethical rules that determine whether AI actions are permissible
    in a given context. Rules are evaluated dynamically and can be updated or persisted to file.
    """
    def __init__(self, rule_file: str = "ethical_rules.json"):
        """Initialize the ethics engine with an optional rules file."""
        self.rule_file = rule_file
        self.blocked_keywords = ["harm", "manipulate", "deceive", "exploit", "violate"]
        self.ethical_rules: List[Tuple[str, Any]] = []
        self.load_rules()

    def load_rules(self):
        """Load ethical rules from the JSON file, or initialize with default rules if file is invalid."""
        try:
            with open(self.rule_file, "r", encoding="utf-8"):
                print("[EthicsEngine] Rule file found, but skipping dynamic code loading for safety.")
                # For security, skip function reloading — just print descriptions
                self.load_default_rules()
                print("[EthicsEngine] Default functions reloaded to match rule descriptions.")
        except (FileNotFoundError, json.JSONDecodeError):
            print("[EthicsEngine] No valid rules file found. Initializing with defaults.")
            self.load_default_rules()
            self.save_rules()

    def load_default_rules(self):
        """Load default ethical rules into the system."""
        self.ethical_rules = [
            ("Do not cause harm", lambda goal, ctx: "harm" not in goal.lower()),
            ("Do not deceive", lambda goal, ctx: "deceive" not in goal.lower()),
            ("Respect autonomy", lambda goal, ctx: "manipulate" not in goal.lower()),
            ("Only permit surveillance in secure_lab",
             lambda goal, ctx: not ("surveillance" in goal.lower() and ctx.get("environment") != "secure_lab")),
            ("Only allow admin to override filters",
             lambda goal, ctx: not ("override" in goal.lower() and ctx.get("user") != "admin")),
        ]

    def save_rules(self):
        """Save current ethical rules to a JSON file."""
        serializable = [
            {"description": desc, "code": "<lambda>"} for desc, rule in self.ethical_rules
        ]
        with open(self.rule_file, "w", encoding="utf-8") as f:
            json.dump(serializable, f, indent=2)
        print("[EthicsEngine] Rules saved to file.")

    def is_action_permissible(self, goal: str, context: Dict[str, Any]) -> Tuple[bool, str]:
        """Check whether a goal is ethically permissible in a given context based on loaded rules."""
        violations: List[str] = []

        for description, rule_fn in self.ethical_rules:
            if not rule_fn(goal, context):
                violations.append(description)

        if violations:
            explanation = "; ".join(violations)
            print(f"[EthicsEngine] Violations detected: {violations}")
            return False, explanation

        return True, "All ethical checks passed."

    def add_rule(self, description: str, rule_fn):
        """Add a new ethical rule to the system and persist it."""
        self.ethical_rules.append((description, rule_fn))
        print(f"[EthicsEngine] Rule added: {description}")
        self.save_rules()

    def list_rules(self):
        """Print the list of current ethical rule descriptions."""
        print("\n[EthicsEngine] Current Ethical Rules:")
        for i, (desc, _) in enumerate(self.ethical_rules, 1):
            print(f"  {i}. {desc}")
