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

buffer = True
"""Buffer stdout and stderr during tests"""

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
    result = next(Path('.').rglob("__init__.py"), None)
    if not result:
        print('__init__.py not found')
        exit(1)
    return result


def suite() -> unittest.TestSuite:
    """Can be imported into `setup.py` as `test_suite="test_unit.suite"`.
    But sadly it's deprecated."""

    return unittest.TestLoader().discover(
        top_level_dir=top_level_dir,
        start_dir=start_dir or str(init_py().parent),
        pattern=pattern)


def run() -> unittest.TestResult:
    """Discovers and runs unit tests for the module."""

    if deps:
        if subprocess.call([sys.executable, "-m", "pip", "install"] + deps) != 0:
            exit(1)

    result = unittest.TextTestRunner(buffer=buffer, verbosity=verbosity, failfast=failfast,
                                     warnings=warnings.value).run(suite())

    if result.failures or result.errors:
        exit(1)

    return result


def main_entry_point():
    run()
