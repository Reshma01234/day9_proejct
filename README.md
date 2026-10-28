# Day 9 – Expense Tracker with JSON Persistence

AhamVerse Technologies – Python Development, Day 9: File Handling & Data Persistence with JSON.
The Day 8 Expense Tracker, extended so expenses are saved to a JSON file and are still there after the program is restarted.

## How to run

From inside `day9_project` (the folder that contains `expense_tracker`):

```
python -m expense_tracker.main
```

On systems that use `python3`:

```
python3 -m expense_tracker.main
```

Requires Python 3 only. Uses only the standard library (`json`, `pathlib`, `os`).

## Where the data is saved

```
day9_project/expenses.json
```

The file is created in the project root (next to the `expense_tracker` folder) the first time an expense is added. The path is built from the code's own location, so it is the same wherever you start the program from. `expenses.sample.json` shows the format. The live `expenses.json` is listed in `.gitignore` because it is personal runtime data.

Example of the saved format:

```json
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

## Project structure

```
day9_project/
├── expense_tracker/
│   ├── __init__.py        # marks the folder as a package (empty)
│   ├── main.py            # menu loop, loads on start, saves after each add, error messages
│   ├── expenses.py        # add, view, calculate and show total
│   ├── validation.py      # validates descriptions, amounts and saved records
│   └── storage.py         # load_expenses(path) and save_expenses(expenses, path)
├── practice_exercises/    # Exercises 1-4
├── import_safety_test.py  # Exercise 5
├── test_scenarios.py      # runs the testing checklist
├── expenses.sample.json
├── day9_notes.txt
├── TEST_RESULTS.md
└── README.md
```

`storage.py` keeps all file code in one place, so `expenses.py` and `validation.py` stay free of file handling. Imports go one way: `main.py` → `expenses.py` / `storage.py` → `validation.py`, with no circular imports.

## How it behaves

| Situation | What happens |
|---|---|
| First run, no `expenses.json` | Starts with an empty list, no error |
| Expense added | Saved to `expenses.json` straight away |
| Restart | Saved expenses are loaded and listed |
| File contains invalid JSON (or is empty) | Clear error message, file is **not** changed, program stops |
| File is valid JSON but the wrong shape | Clear error message, file is **not** changed, program stops |
| Saving fails (for example permissions) | Warning shown, expense kept for this session, program keeps running |
| EOF or Ctrl+C | Exits cleanly, no traceback |

Saving writes to a temporary file first and then replaces `expenses.json`, so a failure part-way through cannot leave a half-written file.

## Validation rules

- Description cannot be blank.
- Amount must be numeric, finite (not `nan`, `inf`, `-inf`) and not negative.
- **Zero is accepted**; only negative amounts are rejected.
- Invalid menu choices show a message and the menu continues.

## Practice exercises

| Exercise | File | What it shows |
|---|---|---|
| 1. Text file | `practice_exercises/ex1_text_file.py` | Write 3 lines, read them back, append a line (`w`, `r`, `a`) |
| 2. JSON round trip | `practice_exercises/ex2_json_round_trip.py` | `json.dump()` then `json.load()`, data comes back identical |
| 3. Missing file | `practice_exercises/ex3_missing_file.py` | `FileNotFoundError` handled as a first run |
| 4. Corrupted JSON | `practice_exercises/ex4_corrupted_json.py` | `json.JSONDecodeError` caught, original file left untouched |
| 5. Import safety | `import_safety_test.py` | Importing the package does not start the menu |

Run Exercises 1-4 with `python practice_exercises/ex1_text_file.py` (and so on). Run Exercise 5 from the project root with `python import_safety_test.py`.

## Testing

```
python test_scenarios.py
```

Runs the full testing checklist (19 checks). Each test uses a fresh copy of the package in a temporary folder, so your real `expenses.json` is never touched. Results are in `TEST_RESULTS.md`.

## Author

Reshma – [github.com/Reshma01234](https://github.com/Reshma01234)
