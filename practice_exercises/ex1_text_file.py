"""Exercise 1 - Text file: write three lines, read them back, append one more."""

from pathlib import Path

NOTES = Path(__file__).resolve().parent / "notes.txt"

# "w" creates the file (or replaces it if it exists)
with open(NOTES, "w", encoding="utf-8") as file:
    file.write("Line 1: files store data after the program ends\n")
    file.write("Line 2: with open() closes the file automatically\n")
    file.write("Line 3: mode 'w' replaces old content\n")

print("--- after writing 3 lines ---")
with open(NOTES, "r", encoding="utf-8") as file:
    print(file.read(), end="")

# "a" adds to the end without removing anything
with open(NOTES, "a", encoding="utf-8") as file:
    file.write("Line 4: mode 'a' appends to the end\n")

print("--- after appending 1 line ---")
with open(NOTES, "r", encoding="utf-8") as file:
    for number, line in enumerate(file, start=1):
        print(f"{number}: {line.rstrip()}")
