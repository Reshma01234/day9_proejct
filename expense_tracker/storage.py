"""Saving and loading expenses as JSON.

The data file is stored in the project root, next to the expense_tracker
folder:

    day9_project/expenses.json

The path is built from this file's own location, so it is the same no matter
which folder the program is started from.
"""

import json
import os
from pathlib import Path

from expense_tracker.validation import is_valid_expense

DATA_FILE = Path(__file__).resolve().parent.parent / "expenses.json"


def load_expenses(path=DATA_FILE):
    """Return the saved expenses as a list of dictionaries.

    - File missing (first run): returns an empty list.
    - Invalid JSON: json.JSONDecodeError is raised (nothing is changed).
    - Valid JSON but wrong shape: ValueError is raised.
    - Other file problems (permissions etc.): OSError is raised.
    The caller decides how to report the problem. This function never
    writes to the file, so damaged data is never overwritten here.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []

    if not isinstance(data, list) or not all(is_valid_expense(item) for item in data):
        raise ValueError(
            "the file must contain a list of expenses, each with a "
            "non-blank 'description' and a valid 'amount'"
        )
    return data


def save_expenses(expenses, path=DATA_FILE):
    """Write the expenses to the JSON file.

    The data is first written to a temporary file and then moved over the
    real file, so a failure part-way through cannot leave a half-written
    expenses.json behind.
    """
    path = Path(path)
    temp_path = path.with_name(path.name + ".tmp")
    with open(temp_path, "w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4, allow_nan=False)
        file.write("\n")
    os.replace(temp_path, path)
