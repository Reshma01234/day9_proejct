"""Entry point for the Expense Tracker.

Run from the day9_project folder with:
    python -m expense_tracker.main
"""

import json

from expense_tracker.expenses import add_expense, show_total, view_expenses
from expense_tracker.storage import DATA_FILE, load_expenses, save_expenses


def show_menu():
    """Print the menu options."""
    print("\n=== Expense Tracker ===")
    print("1. Add expense")
    print("2. View expenses")
    print("3. Show total")
    print("4. Exit")


def load_saved_expenses():
    """Load saved expenses. Return None (after explaining why) if that is not possible."""
    try:
        return load_expenses(DATA_FILE)
    except json.JSONDecodeError as error:
        print(f"Error: {DATA_FILE} is not valid JSON ({error}).")
    except ValueError as error:
        print(f"Error: {DATA_FILE} has unexpected contents: {error}.")
    except OSError as error:
        print(f"Error: could not read {DATA_FILE} ({error}).")
    print("Your data file has NOT been changed. Fix or move the file, then start again.")
    return None


def save_current_expenses(expenses):
    """Save expenses; report a problem instead of crashing."""
    try:
        save_expenses(expenses, DATA_FILE)
    except OSError as error:
        print(f"Warning: could not save to {DATA_FILE} ({error}).")
        print("The expense is kept for this session only.")


def main():
    """Run the menu loop until the user exits."""
    expenses = load_saved_expenses()
    if expenses is None:
        return
    if expenses:
        print(f"Loaded {len(expenses)} saved expense(s).")

    try:
        while True:
            show_menu()
            choice = input("Choose an option (1-4): ").strip()

            if choice == "1":
                add_expense(expenses)
                save_current_expenses(expenses)
            elif choice == "2":
                view_expenses(expenses)
            elif choice == "3":
                show_total(expenses)
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3 or 4.")
    except (EOFError, KeyboardInterrupt):
        print("\nInput ended. Exiting Expense Tracker. Goodbye!")


if __name__ == "__main__":
    main()
