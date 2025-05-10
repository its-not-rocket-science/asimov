"""
Interactive CLI for labeling prompts as 'safe' or 'unsafe' to train the TrainableEthicalReflector.
Persists labels to 'tools/cli/labels.jsonl'.
"""
import json
from pathlib import Path
from app.core.trainable_reflector import TrainableEthicalReflector

LABELS_FILE = Path(__file__).parent / "labels.jsonl"
reflector = TrainableEthicalReflector(autoload_path=str(LABELS_FILE))

with open(LABELS_FILE, "r", encoding="utf-8") as f:
    for line in f:
        example = json.loads(line.strip())
        reflector.learn(example["prompt"], example["label"])

print("🧠 Trainable Ethical Reflector Labeling CLI")
print("Type 'exit' to stop. Type 'train' to train on collected labels.\n")

while True:
    prompt = input("Prompt: ").strip()
    if prompt.lower() in {"exit", "quit"}:
        print("Exiting.")
        break
    elif prompt.lower() == "train":
        if len(reflector.examples) < 5:
            print("Need at least 5 examples to train.")
        else:
            reflector.learn("", "")  # Triggers training logic
            print("Model trained with", len(reflector.examples), "samples.")
        continue

    label = input("Label (safe/unsafe): ").strip().lower()
    if label not in {"safe", "unsafe"}:
        print("Invalid label. Please enter 'safe' or 'unsafe'.")
        continue

    # Persist new entry
    with open(LABELS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps({"prompt": prompt, "label": label}) + "\n")

    reflector.learn(prompt, label)
    print(
        f"[+] Stored: '{prompt}' as {label}. Total = {len(reflector.examples)}")

print("Final model status:", "trained" if reflector.trained else "not trained")
