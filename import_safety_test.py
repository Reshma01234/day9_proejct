"""Exercise 5 - Import safety: importing the package must not start the menu.

Run from the project root:  python import_safety_test.py
If the menu started, the program would wait for input (and this script would
hang or print the menu). It should print only the lines below.
"""

import expense_tracker.main
import expense_tracker.expenses
import expense_tracker.storage
import expense_tracker.validation

print("Imported all modules without starting the menu.")
print("main() exists but has not been called:", callable(expense_tracker.main.main))
