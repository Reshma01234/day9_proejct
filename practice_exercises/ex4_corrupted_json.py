"""Exercise 4 - Corrupted JSON: report it, and do NOT destroy the file."""

import json
from pathlib import Path

BAD = Path(__file__).resolve().parent / "corrupted_expenses.json"
BAD_TEXT = '[{"description": "Lunch", "amount": 180.0},'   # cut off, invalid

BAD.write_text(BAD_TEXT, encoding="utf-8")
before = BAD.read_text(encoding="utf-8")

try:
    with open(BAD, "r", encoding="utf-8") as file:
        data = json.load(file)
except json.JSONDecodeError as error:
    print(f"Could not read {BAD.name}: invalid JSON at line {error.lineno}, "
          f"column {error.colno} ({error.msg}).")
    print("The file was left untouched so the data can be repaired.")

after = BAD.read_text(encoding="utf-8")
print("File content unchanged?", before == after)
BAD.unlink()   # remove the practice file afterwards
