# Asimov

**Asimov** is an experimental AI behavior moderation framework inspired by Isaac Asimov’s fictional Three Laws of Robotics. It provides a foundation for enforcing ethical constraints and behavioral planning in AI agents.

![CI](https://github.com/its-not-rocket-science/asimov/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/its-not-rocket-science/asimov/branch/main/graph/badge.svg)](https://codecov.io/gh/its-not-rocket-science/asimov)

---

## ✅ Current Capabilities: Rule-Based Prompt Filtering

This system currently performs basic behavior moderation based on predefined ethical rules:

- **Manually defined rule functions**, such as:
  - "Do not cause harm" → Blocks prompts containing `"harm"`
  - "Only admins can override" → Prevents unauthorized override attempts
- **Keyword-based filtering** using simple string checks
- **Lambda functions** to encode logical checks for each rule
- **Meta-monitor** layer provides high-level safeguards (e.g., contextual overrides, environment checks)
- **Feedback loop** stores decisions and user interactions for reflection

> The system acts as ethical guardrails around a planner — powered by human-curated rules.


## 🧠 Limitations

- Does **not yet understand semantic meaning** of prompts
- Relies on **exact keywords**, not paraphrased or implied concepts
- Feedback data is stored, but **not yet used to retrain or adapt rules dynamically**


## 🚀 Research & Development Goal: Ethical Behavior Embedding

In addition to layered filters, a major goal is to **integrate ethical reasoning directly into the AI model** itself.

This ensures that even if outer safeguards (filters, policies) are bypassed, the model is internally aligned to reject harmful, deceptive, or manipulative behaviors.

### How We Might Approach This:

- **Train on ethically annotated datasets**: Use RLHF or supervised learning with examples labeled for safety, honesty, and fairness.
- **Incorporate a written 'constitution'**: Similar to Anthropic’s Constitutional AI, define principles the model adheres to during training and inference.
- **Embed ethical concepts in latent space**: Align model representations with concepts like harm, consent, and deception.
- **Reinforcement learning on ethical outcomes**: Apply rewards/penalties based on ethical quality of responses.
- **Introduce reflective reasoning**: Encourage the model to self-check or justify decisions using moral reasoning chains.

This R&D path moves us toward **deep alignment**: building systems that behave ethically not just because they're told to — but because they understand and prefer to.

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

## 🔧 How to Run
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
│   ├── core/           # Ethics, memory, planning, monitoring
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

Want help integrating smarter models or extending planning capabilities? Open an issue or contribute!
