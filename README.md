[![CircleCI](https://circleci.com/gh/Meeqan/trisixty-buys-API.svg?style=svg)](https://circleci.com/gh/Meeqan/trisixty-buys-API)
[![Maintainability](https://api.codeclimate.com/v1/badges/1934168062de29d65434/maintainability)](https://codeclimate.com/github/Meeqan/trisixty-buys-API/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/1934168062de29d65434/test_coverage)](https://codeclimate.com/github/Meeqan/trisixty-buys-API/test_coverage)

# Trisixty-buys-API-Flask
A side project called Trisixty made with Python


### Git Commit Hook
Git pre-commit hook to check staged Python files for formatting issues with
yapf.

INSTALLING:
 Option 1: Copy this file into `.git/hooks/pre-commit`, and mark it as
           executable.
           You will need to do this every time the pre-commit hook is changed.
 Option 2: Create a file `.git/hooks/pre-commit` then create a symlink to
           this file by running the command:
           `ln -s -f ../../hooks/pre-commit .git/hooks/pre-commit`
           You will only need to do this once for your local repository.

 This requires that yapf is installed and runnable in the environment running
 the pre-commit hook.

 When running, this first checks for unstaged changes to staged files, and if
 there are any, it will exit with an error. Files with unstaged changes will be
 printed.

 If all staged files have no unstaged changes, it will run yapf against them,
 leaving the formatting changes unstaged. Changed files will be printed.

 BUGS: This does not leave staged changes alone when used with the -a flag to
 git commit, due to the fact that git stages ALL unstaged files when that flag
 is used.
