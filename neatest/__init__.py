# SPDX-FileCopyrightText: (c) 2021 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT


import subprocess
import sys
from enum import Enum
from typing import List, Optional
import unittest
from pathlib import Path


class NeatestError(Exception):
    def __init__(self, message: str):
        self.message = message


class InstallationError(NeatestError):
    def __init__(self):
        super().__init__("Failed to install test dependencies.")


class TestsError(NeatestError):
    def __init__(self):
        super().__init__("Testing was unsuccessful.")


################################################################################

def contains_parent(possible_parents: List[Path], possible_child: Path) -> bool:
    child_str = str(possible_child.absolute())
    for p in possible_parents:
        if child_str.startswith(str(p.absolute())):
            return True
    return False


def find_start_dirs(start_from: Path = None) -> List[Path]:
    if not start_from:
        start_from = Path('.')
    start_from = start_from.absolute()
    dirs = []
    for file in start_from.rglob("__init__.py"):
        rel = file.relative_to(start_from)
        # skipping files in hidden dirs, like '.venv/**/__init__.py'
        # or '.tox/**/__init__.py'
        if any(str(p).startswith('.') for p in rel.parts):
            continue
        dirs.append(
            (len(file.parent.relative_to(start_from).parts), file.parent))

    if not dirs:
        raise NeatestError('Cannot find __init__.py in current directory.')

    result_paths = []
    for _, dir_path in dirs:
        if not contains_parent(result_paths, dir_path):
            result_paths.append(dir_path)

    return result_paths


class Warnings(Enum):
    # https://www.geeksforgeeks.org/warnings-in-python/
    default = "default"
    error = "error"
    ignore = "ignore"
    always = "always"
    module = "module"
    once = "once"


def run(
        deps: Optional[List[str]] = None,
        pattern: str = '*.py',
        start_dirs: Optional[List[str]] = None,
        top_level_dir: Optional[str] = '.',
        buffer=False,
        failfast=False,
        verbosity=1,
        exit_if_failed=True,
        warnings: Warnings = Warnings.default
) -> List[unittest.TestResult]:
    """Discovers and runs unit tests for the module.
    deps: Dependent modules to install with pip install before running tests.
    These are modules that are used for testing but are not needed in production
    code. Therefore, they are expectedly missing from requirements.txt and
    setup.py.

    pattern: Mask for the names of the files that contain the tests.

    start_dir: Directory to start discovery. None means the first found
    directory with '__init__.py' inside, starting recursive search from the
    current directory.

    top_level_dir: Top level directory of project (defaults to current
    directory). None will set to the same value as `start_dir`.

    buffer: Buffer stdout and stderr during tests

    failfast: Stop on first fail or error

    verbosity: 0 for quiet, 2 for verbose
    """

    try:

        if deps:
            if subprocess.call(
                    [sys.executable, "-m", "pip", "install"] + deps) != 0:
                raise InstallationError

        # if start_dir is not None:
        if start_dirs is None:
            start_dirs = [str(p) for p in find_start_dirs()]

        results = []

        for sd in start_dirs:
            print(f"start_dir: {sd}")

            suite = unittest.TestLoader().discover(
                top_level_dir=top_level_dir,
                start_dir=sd,
                pattern=pattern)

            result = unittest.TextTestRunner(buffer=buffer, verbosity=verbosity,
                                             failfast=failfast,
                                             warnings=warnings.value).run(suite)

            results.append(result)

        if exit_if_failed and any(
                not result.wasSuccessful() for result in results):
            raise TestsError
        return results

    except NeatestError as e:
        print(e.message)
        if exit_if_failed:
            sys.exit(1)

    # alternatively we could run the tests exactly as '-m unittest' does
    # with unittest.TestProgram(module=None, argv)
    # where argv is ['python -m unittest', 'discover', ...]


def main_entry_point():
    run()
