"""Exercise 2 - JSON round trip: dump a list of expenses, load it back."""

import json
from pathlib import Path

SAMPLE = Path(__file__).resolve().parent / "sample_expenses.json"

expenses = [
    {"description": "Lunch", "amount": 180.0},
    {"description": "Bus ticket", "amount": 35.5},
    {"description": "Notebook", "amount": 60.0},
]

with open(SAMPLE, "w", encoding="utf-8") as file:
    json.dump(expenses, file, indent=4)

with open(SAMPLE, "r", encoding="utf-8") as file:
    loaded = json.load(file)

print("Loaded data:", loaded)
print("Same as original?", loaded == expenses)
print("Type of loaded data:", type(loaded).__name__)
