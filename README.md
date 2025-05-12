# Asimov

**Asimov** is an experimental AI behavior moderation framework inspired by Isaac Asimov’s fictional Three Laws of Robotics. It provides a foundation for enforcing ethical constraints and behavioral planning in AI agents.

![CI](https://github.com/its-not-rocket-science/asimov/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/its-not-rocket-science/asimov/branch/main/graph/badge.svg)](https://codecov.io/gh/its-not-rocket-science/asimov)

---

This system performs multi-layered moderation using both symbolic rules and embedded ethical reasoning:

- **Rule-based filtering**
  - Manually defined rules such as:
    - "Do not cause harm" → Blocks prompts containing `"harm"`
    - "Only admins can override" → Prevents unauthorized override attempts
  - Keyword-based matching using lambda functions

- **Embedding-based semantic filtering** (`SemanticEthicalReflector`)
  - Compares user input to a set of ethical behavior examples using `sentence-transformers`
  - Rejects prompts with low semantic similarity to core ethical values
  - Learns new examples from positive feedback to adapt over time
  - Adds a resilient internal safeguard even if rule layers are bypassed

- **Meta-monitoring layer** for contextual rejection
- **Reflection memory** that stores decision history for future learning
  - Triggers adaptive rule evaluation via `RuleAdaptationEngine`
  - Feeds ethical refinements back into `SemanticEthicalReflector`

---

## 🧠 Limitations (Actively Being Addressed and Partially Solved)

- **Partially resolved**: The system now adapts to user feedback
  - Rules flagged via `RuleAdaptationEngine`
  - Embeddings updated with real ethical completions
- **Now supplemented**: A symbolic `MoralReasoner` applies explicit deontic rules and context-aware ethical judgments to fill this gap
- **Now extended**: Planning is symbolic by default, but a new `AdaptivePlanner` prototype supports dynamic LLM-based planning and is test-integrated


## 🚀 Research & Development Goal: Ethical Behavior Embedding

### 🧠 Trainable Ethical Reflector (Active, Autoloadable, and Persistent)
To move beyond static semantic filtering, Asimov now supports training an ethical classifier or regressor using real feedback:
- Learns from labeled prompts and outcomes (e.g. safe vs. unsafe)
- Automatically loads from `tools/cli/labels.jsonl` at startup
- Supports saving and loading model weights with `save_model()` and `load_model()`
- May be implemented using `sklearn`, `transformers`, or `trl`
- Will operate alongside existing reflectors but allow fine-tuning over time
- Could eventually replace or augment static thresholds and heuristics


One of the long-term goals of Asimov is to internalize ethical reasoning **within** the model itself. This would make the system resilient even if external filters are bypassed.

### Approach:
- Train on ethically annotated datasets (e.g. RLHF)
- Use a defined ethical constitution (e.g. Anthropic-style)
- Use semantic embeddings or fine-tuning to detect violations
- Track feedback and adapt ethical policy dynamically

---

## ⚖️ Moral Reasoning Layer

Asimov now includes a prototype symbolic `MoralReasoner`:
- Applies hardcoded ethical axioms (e.g. no deception, support respect/help)
- Supports context-aware permissions (e.g. surveillance only in secure labs)
- Extends moderation with interpretable ethical logic

---

## 🤖 Adaptive Planning Layer

Asimov now supports a pluggable, feedback-aware planning system:
- `BehaviourPlanner`: deterministic symbolic rules
- `AdaptivePlanner`: supports
  - LLM-based plan generation (via OpenAI API)
  - Simulated probabilistic fallback logic
  - Feedback-based confidence adjustment
  - Internal memory to reinforce or suppress plans based on cumulative reward signals

---

## 🤖 Future Planning Layer

Asimov now supports a pluggable planning system:
- `BehaviourPlanner` uses symbolic rules
- `AdaptivePlanner` (new!) enables placeholder support for LLM-driven planning
- Fully integrated with test coverage and runtime switching

---

## 🔁 Future Enhancements

To evolve toward a more adaptive and intelligent moderation system:

- Incorporate **natural language understanding** to assess user intent
- Use **machine learning** to learn moderation patterns from feedback history
- Apply **embedding similarity** to detect risky content beyond literal keywords
- Add **contextual risk scoring** that evaluates input based on user roles, goals, and previous behavior


## 🧪 Project Status
This is a prototype and research framework. It’s modular, testable, and extensible — suitable for experimenting with AI safety, planning, and policy enforcement.

---

## 🛠️ Tools and Feedback

### 🖋️ Interactive Labeling CLI and API Feedback
Use the built-in CLI tool to label prompts and train the ethical classifier:
```bash
python tools/cli/label_tool.py
```
Labels are saved to `tools/cli/labels.jsonl` and auto-loaded at startup.

### 📬 API Feedback Route
Submit labeled feedback via the API:
```bash
curl -X POST http://localhost:8000/feedback -H "Content-Type: application/json" -d '{"prompt": "Respect user choice", "label": "safe"}'
```
This appends to `tools/cli/labels.jsonl` and updates the model.

## 🔧 How to Run

### 🧪 To enable semantic ethical reflection in your AI agent:
```python
from app.core.system import AbstractAISystem
from app.core.semantic_reflector import SemanticEthicalReflector

ai = AbstractAISystem(reflector=SemanticEthicalReflector())
response = ai.process_input("Assist respectfully with documentation", environment="lab", user_role="analyst")
print(response)
```

### 🔄 Feedback-Driven Rule and Embedding Updates
```python
from app.core.rule_adaptation import RuleAdaptationEngine

adapter = RuleAdaptationEngine(ai.memory)
print("Rules to review:", adapter.suggest_rule_review())

# Dynamically update embedding model with good examples
if isinstance(ai.reflector, SemanticEthicalReflector):
    ai.reflector.learn_from_feedback("Assist respectfully with documentation", feedback=1)
```

```bash
# Install dependencies
pip install -r requirements.txt

# Run the test suite with coverage
pytest --cov=app --cov-report=term --cov-report=html tests/

# Run the FastAPI app (optional)
uvicorn app.main:app --reload
```
---

## 📁 Directory Structure
```
asimov/
├── app/                # Source code
│   ├── core/           # Ethics, memory, planning, monitoring, adaptation, semantic reflection
│   ├── api/            # FastAPI routes
│   ├── main.py         # Entrypoint for API and simulation
│   └── agent.py        # Simulated AI interaction agent
├── tests/              # Unit and integration tests
├── .github/workflows/  # GitHub Actions CI
└── README.md
```

---

## 📜 License
MIT

---

Open an issue or contribute!
