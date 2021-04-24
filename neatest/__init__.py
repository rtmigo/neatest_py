# SPDX-FileCopyrightText: (c) 2021 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT


import subprocess
import sys
from enum import Enum
from typing import List, Optional
import unittest
from pathlib import Path

# CONFIGURABLE OPTIONS #######################################################

deps: Optional[List[str]] = None
"""Dependent modules to install with pip install before running tests.
These are modules that are used for testing but are not needed in production 
code. Therefore, they are expectedly missing from requirements.txt and setup.py.
"""

pattern: str = '*.py'
"""Mask for the names of the files that contain the tests."""

start_dir: Optional[str] = None
"""Directory to start discovery. None means the first found directory with 
'__init__.py' inside, starting recursive search from the current directory."""

top_level_dir: Optional[str] = '.'
"""Top level directory of project (defaults to current directory).
None will set to the same value as `start_dir`."""

buffer = False
"""Buffer stdout and stderr during tests"""
# when we set this to True, it hides valuable resource warnings

failfast = False
"""Stop on first fail or error"""

verbosity = 1
"""0 for quiet, 2 for verbose"""


class Warnings(Enum):
    # https://www.geeksforgeeks.org/warnings-in-python/
    default = "default"
    error = "error"
    ignore = "ignore"
    always = "always"
    module = "module"
    once = "once"


warnings: Warnings = Warnings.default


################################################################################


def init_py() -> Path:

    parent = Path('.').absolute()

    for file in parent.rglob("__init__.py"):
        rel = file.relative_to(parent)
        # skipping files in hidden dirs, like '.venv/**/__init__.py'
        # or '.tox/**/__init__.py'
        if any(str(p).startswith('.') for p in rel.parts):
            continue
        return file

    print('__init__.py not found')
    exit(1)



def suite() -> unittest.TestSuite:
    """Can be imported into `setup.py` as `test_suite="test_unit.suite"`.
    But sadly it's deprecated."""

    return unittest.TestLoader().discover(
        top_level_dir=top_level_dir,
        start_dir=start_dir or str(init_py().parent),
        pattern=pattern)


def __run_as_program():
    # alternatively we can run the tests exactly as '-m unittest' does

    argv = [sys.executable + ' -m unittest', 'discover', '-p', pattern, '-s', start_dir or str(init_py().parent), '-t',
            top_level_dir]

    return unittest.TestProgram(module=None,
                                exit=False,
                                verbosity=verbosity,
                                failfast=failfast,
                                buffer=buffer,
                                argv=argv).result


def run() -> unittest.TestResult:
    """Discovers and runs unit tests for the module."""

    if deps:
        if subprocess.call([sys.executable, "-m", "pip", "install"] + deps) != 0:
            exit(1)

    result = unittest.TextTestRunner(buffer=buffer, verbosity=verbosity, failfast=failfast,
                                     warnings=warnings.value).run(suite())

    if not result.wasSuccessful():
        exit(1)

    return result


def main_entry_point():
    run()
