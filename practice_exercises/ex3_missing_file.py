"""Exercise 3 - Missing file: treat it as a first run, no traceback."""

import json
from pathlib import Path

MISSING = Path(__file__).resolve().parent / "does_not_exist.json"


def load_or_empty(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"{path.name} not found - first run, starting with an empty list.")
        return []


print("File exists?", MISSING.exists())
data = load_or_empty(MISSING)
print("Result:", data)
