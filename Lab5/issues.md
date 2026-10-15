# Issues Found and Fixed — `energy_system.py`

Line numbers refer to the **original** starter file. Ordered by severity (high/medium first).

| # | Issue | Type | Tool / Code | Line(s) | Description | Fix Approach |
|---|-------|------|-------------|---------|-------------|--------------|
| 1 | Use of `eval()` on user input | Security (Medium sev, High conf) | Bandit B307, Pylint W0123 | 62–63 | `input()` was passed straight to `eval()`, so a user could run arbitrary Python (e.g. `__import__('os').system(...)`). | Parse the input with `float()` inside `try/except ValueError`; invalid input falls back to 0. |
| 2 | Mutable default argument | Bug | Pylint W0102 | 12 | `history=[]` is created once and shared by every call that uses the default, so readings from earlier calls stay in the list and leak into later ones. | Default to `None`, create a new list inside the function; `main()` now passes one explicit history list. |
| 3 | Negative readings accepted | Logic bug (not flagged by tools) | — (found by running the program) | 55, 13–14 | `record_reading("M-03", -50)` was stored, giving a bill of **-192.50**. A meter cannot report negative usage. | `record_reading` raises `ValueError` for `units < 0`; `main()` catches it and prints "Rejected". |
| 4 | Bare `except:` | Bug / Bad practice | Pylint W0702, Flake8 E722 | 44 | Catches everything, including `KeyboardInterrupt` and typos, and silently wipes the data. | Catch only `FileNotFoundError` and `json.JSONDecodeError`. |
| 5 | Files opened without `with` / encoding | Resource leak | Pylint R1732, W1514 | 42, 48 | `load_meter_data` never closed its file; neither call set an encoding. | Use `with open(..., encoding="utf-8")` and `json.load` / `json.dump`. |
| 6 | `global` statements | Design | Pylint W0603 | 27, 40 | `raise_rates` mutated module constants (calling it twice compounds the rise); `load_meter_data` rebound `meters`. | `raise_rates(rates, percent)` now returns a new list; `load_meter_data` updates `meters` in place with `clear()` + `update()`. |
| 7 | Unused import `sys` | Code quality | Pylint W0611, Flake8 F401 | 2 | Imported but never used. | Removed. |
| 8 | Missing docstrings | Style | Pylint C0114, C0116 | 1, 12, 17, 26, 32, 39, 47, 52 | No module or function docstrings. | Added a docstring to the module and every function. |
| 9 | `%` string formatting | Style | Pylint C0209 | 59, 60, 66 | Old-style formatting. | Converted to f-strings. |
| 10 | `elif` after `return` | Style | Pylint R1705 | 19–24 | Unnecessary `elif`/`else` after `return`. | Replaced with plain `if` and a final `return`. |
| 11 | Code runs on import | Design | — | 68 | `main()` ran whenever the module was imported. | Wrapped in `if __name__ == "__main__":`. |
| 12 | Blank lines between definitions | Style (PEP 8) | Flake8 E302, E305 | 12, 17, 26, 32, 39, 47, 52, 68 | One blank line instead of two around top-level functions. | Two blank lines before each top-level `def` and the `__main__` block. |
| 13 | Lines too long | Style (PEP 8) | Flake8 E501 | 24, 62 | Lines of 88 and 86 characters (limit 79). | Wrapped the expressions in parentheses over two lines; shortened the prompt. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 6.14/10 (22 messages) | **10.00/10** |
| Bandit | 1 Medium (B307) | **No issues identified** |
| Flake8 | 12 warnings | **0 warnings** |
