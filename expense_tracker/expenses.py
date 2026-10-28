"""Expense operations: add, view, and total.

Expenses are kept in a plain list of dictionaries that main.py owns and
passes in, for example: {"description": "Tea", "amount": 20.0}.
"""

from expense_tracker.validation import get_amount, get_description


def add_expense(expenses):
    """Ask for a description and amount, then store the expense."""
    description = get_description()
    amount = get_amount()
    expenses.append({"description": description, "amount": amount})
    print(f"Added: {description} - {amount:.2f}")


def view_expenses(expenses):
    """Print every stored expense with a number."""
    if not expenses:
        print("No expenses recorded yet.")
        return

    print("\n--- Expenses ---")
    for number, expense in enumerate(expenses, start=1):
        print(f"{number}. {expense['description']} - {expense['amount']:.2f}")


def calculate_total(expenses):
    """Return the sum of all expense amounts."""
    return sum(expense["amount"] for expense in expenses)


def show_total(expenses):
    """Print the total of all expenses."""
    print(f"Total expenses: {calculate_total(expenses):.2f}")
