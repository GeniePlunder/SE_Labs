# Reflection — Lab 5: Static Code Analysis

### 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest were the Flake8 style warnings and the simple Pylint messages: removing the unused `sys` import, adding a second blank line between functions, switching to f-strings and adding docstrings. Each is a mechanical, local change with no effect on behaviour.

The hardest were the `global-statement` warnings and the mutable default argument, because fixing them meant changing how data flows through the program rather than editing a single line. `raise_rates` had to return new rates instead of modifying module constants, `load_meter_data` had to update the shared dictionary in place, and `main()` had to pass an explicit history list. I had to rerun the program after each change to make sure the bills were still the same. Replacing `eval()` also needed some thought: the simple fix is `float()`, but I also had to decide what to do with invalid input instead of letting the program crash.

### 2. Did the static analysis tools report any false positives? If so, describe one example.

There were no clear false positives, but some warnings depend on context. Pylint's `global-statement` warning is a design opinion rather than a bug — in a tiny script a global is workable, though removing it did expose a real problem (calling `raise_rates` twice compounded the rise on the module constants). Flake8's 79-character E501 limit is also a convention many teams relax to 88 or 100; Pylint's own default limit of 100 did not flag those same lines.

The opposite problem was more important: the tools missed real bugs. None of them flagged that a negative reading (`-50`) was accepted and produced a negative bill of -192.50. I only found it by running the program and reading the output, which shows that static analysis does not replace testing.

### 3. How would you integrate static analysis tools into your actual software development workflow?

- **Locally:** run Flake8 and Pylint in the editor so issues appear while typing, and add them as `pre-commit` hooks so code that fails cannot be committed.
- **In CI:** run all three tools on every pull request (e.g. a GitHub Actions job), failing the build on any Bandit Medium/High finding, any Flake8 error, or a Pylint score below an agreed threshold such as 9.5 (`pylint --fail-under=9.5`).
- **Configuration:** keep a shared `.pylintrc` / `setup.cfg` in the repo so everyone uses the same rules, and use targeted inline disables (with a comment explaining why) instead of turning rules off globally.
- **Alongside tests:** combine static analysis with unit tests, since bugs like the negative reading are only caught by checking behaviour.

### 4. What tangible improvements did you observe in code quality, readability, or robustness after applying the fixes?

- **Security:** the `eval()` code-injection hole is gone; typing `__import__('os').getcwd()` is now rejected as "Invalid reading" instead of being executed. Bandit went from 1 Medium issue to none.
- **Correctness:** readings no longer leak between calls through the shared default list, and negative readings are rejected, so M-03's bill is 0.00 instead of -192.50.
- **Robustness:** files are always closed (`with`), use an explicit encoding, and only the expected errors (missing or corrupt JSON) are caught, so real bugs are no longer hidden by a bare `except`.
- **Readability and maintainability:** every function has a docstring, there are no hidden global side effects, and the code follows PEP 8. Pylint rose from 6.14/10 to 10.00/10 and Flake8 reports zero warnings. The module can now also be imported (e.g. for tests) without running `main()`.
