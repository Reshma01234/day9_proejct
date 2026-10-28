"""Input validation helpers for the Expense Tracker.

This module only knows how to ask the user for a value and check it.
It does not import main.py or expenses.py, so there are no circular imports.
"""

import math


def parse_amount(text):
    """Convert text to a float, or return None if it is not a valid amount.

    Valid means: a real, finite, non-negative number.
    Rejected: letters, blank text, nan, inf, -inf and negative numbers.
    """
    try:
        value = float(text)
    except ValueError:
        return None

    if not math.isfinite(value):  # catches nan, inf, -inf
        return None
    if value < 0:
        return None
    return value


def get_description(prompt="Enter description: "):
    """Keep asking until the user types a non-blank description."""
    while True:
        description = input(prompt).strip()
        if description:
            return description
        print("Description cannot be blank. Please try again.")


def get_amount(prompt="Enter amount: "):
    """Keep asking until the user types a valid amount (see parse_amount)."""
    while True:
        amount = parse_amount(input(prompt).strip())
        if amount is not None:
            return amount
        print("Invalid amount. Enter a finite number that is not negative "
              "(for example 250 or 99.50).")


def is_valid_expense(record):
    """Return True if record is a dict with a non-blank description and a valid amount.

    Used when loading saved data, so a hand-edited or damaged file with the
    wrong shape is noticed instead of crashing later.
    """
    if not isinstance(record, dict):
        return False
    description = record.get("description")
    amount = record.get("amount")
    if not isinstance(description, str) or not description.strip():
        return False
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        return False
    return parse_amount(str(amount)) is not None
