# SPDX-FileCopyrightText: (c) 2021 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT


import subprocess
import sys
from typing import List, Optional
import unittest
from pathlib import Path

pattern: str = 'test*.py'
deps: Optional[List[str]] = None
top_level_dir = "."
start_dir: Optional[str] = None


def init_py() -> Path:
    result = next(Path(top_level_dir).rglob("__init__.py"), None)
    if not result:
        print('__init__.py not found')
        exit(3)
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

    result = unittest.TextTestRunner(buffer=True).run(suite())

    if result.failures or result.errors:
        exit(2)

    return result
