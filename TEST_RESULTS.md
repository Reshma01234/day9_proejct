# Test Results - Day 9

Command: `python test_scenarios.py` (each test runs a fresh copy of the package in a temporary folder, so real data is never touched)
Python: Python 3.12.3  |  Date: 2026-10-28

## Checklist outcome

| Checklist item | Test | Result |
|---|---|---|
| Launches with python -m expense_tracker.main | 1 | PASS |
| First launch works with no JSON file | 2 | PASS |
| Add one expense, exit, relaunch, still present | 3 | PASS |
| Multiple expenses, correct total after restart | 4 | PASS |
| Blank description rejected | 5 | PASS |
| Alphabetic amount rejected | 6 | PASS |
| Negative amount rejected | 7 | PASS |
| nan, inf, -inf rejected | 8 | PASS |
| Zero amount follows documented rule (accepted) | 9 | PASS |
| Invalid menu choice handled | 10 | PASS |
| Malformed JSON: clear error, not overwritten | 11, 11b, 11c | PASS |
| Importing modules does not start the menu | 12 | PASS |
| EOF and Ctrl+C handled | 13a, 13b, 13c | PASS |

## Full output
```
[PASS] 1. Launches with python -m expense_tracker.main
[PASS] 2. First launch with no data file: no traceback, empty list
[PASS] 3. Expense persists after restart
[PASS] 4. Total correct after restart (200.50)
[PASS] 5. Blank description rejected
[PASS] 6. Alphabetic amount rejected without crashing
[PASS] 7. Negative amount rejected
[PASS] 8. nan, inf and -inf rejected
[PASS] 9. Zero amount accepted (documented rule: only negative is rejected)
[PASS] 10. Invalid menu choice handled
[PASS] 11. Malformed JSON: clear error and file not overwritten
[PASS] 11b. Valid JSON with wrong structure refused and not overwritten
[PASS] 11c. Empty data file treated as corrupted, not overwritten
[PASS] 12. Importing modules does not start the menu
[PASS] 13a. EOF at menu handled, no traceback
[PASS] 13b. EOF in the middle of adding handled, nothing saved
[PASS] 13c. Ctrl+C handled, no traceback
[PASS] Extra A. Data file path does not depend on the current folder
[PASS] Extra B. Save failure reported clearly, app keeps running

19/19 checks passed
```

## Exercise 5 (import safety)
```
Imported all modules without starting the menu.
main() exists but has not been called: True
```

## Practice exercises 1-4 output
```
===== ex1_text_file.py =====
--- after writing 3 lines ---
Line 1: files store data after the program ends
Line 2: with open() closes the file automatically
Line 3: mode 'w' replaces old content
--- after appending 1 line ---
1: Line 1: files store data after the program ends
2: Line 2: with open() closes the file automatically
3: Line 3: mode 'w' replaces old content
4: Line 4: mode 'a' appends to the end
===== ex2_json_round_trip.py =====
Loaded data: [{'description': 'Lunch', 'amount': 180.0}, {'description': 'Bus ticket', 'amount': 35.5}, {'description': 'Notebook', 'amount': 60.0}]
Same as original? True
Type of loaded data: list
===== ex3_missing_file.py =====
File exists? False
does_not_exist.json not found - first run, starting with an empty list.
Result: []
===== ex4_corrupted_json.py =====
Could not read corrupted_expenses.json: invalid JSON at line 1, column 44 (Expecting value).
The file was left untouched so the data can be repaired.
File content unchanged? True
```

## Saved JSON after adding Tea 20 and Lunch 150.50 (see expenses.sample.json)
```
[
    {
        "description": "Tea",
        "amount": 20.0
    },
    {
        "description": "Lunch",
        "amount": 150.5
    }
]
```
