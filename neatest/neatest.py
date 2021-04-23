# SPDX-FileCopyrightText: (c) 2021 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT


import subprocess
import sys
from typing import List, Optional
import unittest
from pathlib import Path

pattern: str = 'test*.py'
deps: Optional[List[str]] = None


def suite() -> unittest.TestSuite:
    """Can be imported into `setup.py` as `test_suite="test_unit.suite"`.
    But sadly it's deprecated."""

    parent_dir = Path(__file__).parent
    init_py = next(parent_dir.rglob("__init__.py"), None)
    if not init_py:
        print('__init__.py not found')
        exit(3)

    return unittest.TestLoader().discover(
        top_level_dir=str(parent_dir),
        start_dir=str(init_py.parent),
        pattern=pattern)


def run() -> None:
    """Discovers and runs unit tests for the module."""

    if deps:
        if subprocess.call([sys.executable, "-m", "pip", "install"] + deps) != 0:
            exit(1)

    result = unittest.TextTestRunner(buffer=True).run(suite())

    if result.failures or result.errors:
        exit(2)
