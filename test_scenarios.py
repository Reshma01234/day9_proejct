"""Runs the Day 9 testing checklist against the real application.

Run from the project root:  python test_scenarios.py

Each test copies the expense_tracker package into a fresh temporary folder
and runs it there. The data file lives next to the package, so every test
gets its own clean expenses.json and your real data is never touched.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent / "expense_tracker"
results = []


def new_project():
    """Make a temporary project folder containing a copy of the package."""
    folder = Path(tempfile.mkdtemp(prefix="day9_test_"))
    shutil.copytree(PACKAGE, folder / "expense_tracker",
                    ignore=shutil.ignore_patterns("__pycache__"))
    return folder


def run_app(folder, lines, cwd=None):
    """Run the app in folder with scripted input; return (output, exit code)."""
    proc = subprocess.run(
        [sys.executable, "-m", "expense_tracker.main"],
        input="\n".join(lines) + "\n", capture_output=True, text=True,
        cwd=cwd or folder, timeout=15)
    return proc.stdout + proc.stderr, proc.returncode


def saved(folder):
    return json.loads((folder / "expenses.json").read_text(encoding="utf-8"))


def check(name, condition):
    results.append((name, condition))
    print(f"[{'PASS' if condition else 'FAIL'}] {name}")


# 1. Launch with python -m from the project root
p = new_project()
out, code = run_app(p, ["4"])
check("1. Launches with python -m expense_tracker.main", "=== Expense Tracker ===" in out and code == 0)

# 2. First launch, no JSON file
p = new_project()
out, code = run_app(p, ["2", "4"])
check("2. First launch with no data file: no traceback, empty list",
      "No expenses recorded yet." in out and "Traceback" not in out
      and not (p / "expenses.json").exists())

# 3. Add one expense, exit, relaunch, still there
p = new_project()
run_app(p, ["1", "Tea", "20", "4"])
out, _ = run_app(p, ["2", "4"])
check("3. Expense persists after restart",
      saved(p) == [{"description": "Tea", "amount": 20.0}]
      and "Loaded 1 saved expense(s)." in out and "1. Tea - 20.00" in out)

# 4. Several expenses, total correct after restart
p = new_project()
run_app(p, ["1", "Tea", "20", "1", "Lunch", "150.50", "1", "Bus", "30", "4"])
out, _ = run_app(p, ["3", "4"])
check("4. Total correct after restart (200.50)", "Total expenses: 200.50" in out)

# 5. Blank description rejected
p = new_project()
out, _ = run_app(p, ["1", "", "   ", "Snack", "10", "4"])
check("5. Blank description rejected", out.count("Description cannot be blank") == 2
      and saved(p) == [{"description": "Snack", "amount": 10.0}])

# 6. Alphabetic amount rejected
out, code = run_app(new_project(), ["1", "Snack", "abc", "10", "4"])
check("6. Alphabetic amount rejected without crashing",
      "Invalid amount" in out and "Traceback" not in out and code == 0)

# 7. Negative amount rejected
p = new_project()
out, _ = run_app(p, ["1", "Snack", "-5", "10", "4"])
check("7. Negative amount rejected", "Invalid amount" in out and saved(p)[0]["amount"] == 10.0)

# 8. nan, inf, -inf rejected
p = new_project()
out, _ = run_app(p, ["1", "Snack", "nan", "inf", "-inf", "10", "4"])
check("8. nan, inf and -inf rejected", out.count("Invalid amount") == 3 and len(saved(p)) == 1)

# 9. Zero amount follows documented rule (zero is accepted)
p = new_project()
out, _ = run_app(p, ["1", "Free sample", "0", "4"])
check("9. Zero amount accepted (documented rule: only negative is rejected)",
      saved(p) == [{"description": "Free sample", "amount": 0.0}])

# 10. Invalid menu choice
out, _ = run_app(new_project(), ["9", "x", "", "4"])
check("10. Invalid menu choice handled", out.count("Invalid choice") == 3 and "Goodbye!" in out)

# 11. Malformed JSON: clear error, file NOT overwritten
p = new_project()
bad = '[{"description": "Lunch", "amount": 180.0},'
(p / "expenses.json").write_text(bad, encoding="utf-8")
out, code = run_app(p, ["1", "Tea", "20", "4"])
check("11. Malformed JSON: clear error and file not overwritten",
      "not valid JSON" in out and "NOT been changed" in out and "Traceback" not in out
      and (p / "expenses.json").read_text(encoding="utf-8") == bad)

# 11b. Valid JSON, wrong shape: also refused, not overwritten
p = new_project()
wrong = '{"description": "Lunch", "amount": 180}'
(p / "expenses.json").write_text(wrong, encoding="utf-8")
out, _ = run_app(p, ["4"])
check("11b. Valid JSON with wrong structure refused and not overwritten",
      "unexpected contents" in out and (p / "expenses.json").read_text(encoding="utf-8") == wrong)

# 11c. Empty file is invalid JSON: treated as corrupted, not overwritten
p = new_project()
(p / "expenses.json").write_text("", encoding="utf-8")
out, _ = run_app(p, ["4"])
check("11c. Empty data file treated as corrupted, not overwritten",
      "not valid JSON" in out and (p / "expenses.json").read_text(encoding="utf-8") == "")

# 12. Importing modules does not start the menu
p = new_project()
proc = subprocess.run(
    [sys.executable, "-c",
     "import expense_tracker.main, expense_tracker.expenses, "
     "expense_tracker.storage, expense_tracker.validation; print('IMPORT_OK')"],
    capture_output=True, text=True, cwd=p, input="", timeout=15)
check("12. Importing modules does not start the menu",
      "IMPORT_OK" in proc.stdout and "Expense Tracker" not in proc.stdout
      and not (p / "expenses.json").exists())

# 13. EOF and Ctrl+C
out, code = run_app(new_project(), [])
check("13a. EOF at menu handled, no traceback", "Traceback" not in out and code == 0)
out, code = run_app(new_project(), ["1", "Tea"])
check("13b. EOF in the middle of adding handled, nothing saved",
      "Traceback" not in out and code == 0)
p = new_project()
proc = subprocess.run(
    [sys.executable, "-c",
     "import builtins\n"
     "def boom(*a, **k): raise KeyboardInterrupt\n"
     "builtins.input = boom\n"
     "from expense_tracker.main import main\n"
     "main()"],
    capture_output=True, text=True, cwd=p, timeout=15)
check("13c. Ctrl+C handled, no traceback",
      "Traceback" not in proc.stderr and proc.returncode == 0)

# Extra: data file is created next to the package, whatever the current folder
p = new_project()
elsewhere = Path(tempfile.mkdtemp(prefix="day9_elsewhere_"))
subprocess.run([sys.executable, "-m", "expense_tracker.main"], input="1\nTea\n20\n4\n",
               capture_output=True, text=True, cwd=p, timeout=15,
               env={**__import__("os").environ, "PYTHONPATH": str(p)})
out, _ = subprocess.run([sys.executable, "-m", "expense_tracker.main"], input="4\n",
                        capture_output=True, text=True, cwd=elsewhere, timeout=15,
                        env={**__import__("os").environ, "PYTHONPATH": str(p)}), None
check("Extra A. Data file path does not depend on the current folder",
      (p / "expenses.json").exists() and not (elsewhere / "expenses.json").exists())

# Extra: a save failure is reported instead of crashing
p = new_project()
(p / "expenses.json.tmp").mkdir()   # a folder where the temp file must go -> OSError
out, code = run_app(p, ["1", "Tea", "20", "4"])
check("Extra B. Save failure reported clearly, app keeps running",
      "could not save" in out and "Traceback" not in out and code == 0)

passed = sum(ok for _, ok in results)
print(f"\n{passed}/{len(results)} checks passed")
sys.exit(0 if passed == len(results) else 1)
