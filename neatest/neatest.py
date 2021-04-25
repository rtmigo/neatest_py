# SPDX-FileCopyrightText: (c) 2021 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT


import subprocess
import sys
from enum import Enum, IntEnum
from typing import List, Optional, Union, Tuple
import unittest
from pathlib import Path
import neatest.constants


class NeatestError(Exception):
    def __init__(self, message: str):
        self.message = message


class InstallationError(NeatestError):
    def __init__(self):
        super().__init__("Failed to install test dependencies.")


class TestsError(NeatestError):
    def __init__(self):
        super().__init__("Testing was unsuccessful.")


class ModulesNotFoundError(NeatestError):
    def __init__(self, top_level_dir: Path):
        super().__init__(f'Cannot find a module directory (with __init__.py) '
                         f'inside {top_level_dir}')


################################################################################


def find_start_dirs(start_from: Path = None) -> List[Path]:
    if not start_from:
        start_from = Path('.')
    start_from = start_from.absolute()

    # TODO this can be rewritten more effectively with recursion, that does
    # not go deeper once "__init__.py" is found
    dirs = []
    for subdir in start_from.glob("*"):
        if subdir.name.startswith('.'):
            continue
        if not subdir.is_dir():
            continue
        if not (subdir / "__init__.py").exists():
            continue
        dirs.append(subdir)

    if not dirs:
        raise ModulesNotFoundError(start_from)

    return dirs


class Warnings(Enum):
    # https://www.geeksforgeeks.org/warnings-in-python/
    default = "default"
    error = "error"
    ignore = "ignore"
    always = "always"
    module = "module"
    once = "once"


class Verbosity(IntEnum):
    quiet = 0
    normal = 1
    verbose = 2


splitter = '-' * 70


def install_requirements(tests_require: List[str]):
    if subprocess.call(
            [sys.executable, "-m", "pip",
             "install"] + tests_require) != 0:
        raise InstallationError


def run(
        tests_require: Optional[List[str]] = None,
        pattern: str = '*.py',
        start_directory: Optional[Union[str, List[str]]] = None,
        top_level_directory: Optional[str] = '.',
        buffer=False,
        failfast=False,
        verbosity=Verbosity.normal,
        exit_if_failed=True,
        warnings: Warnings = Warnings.default
) -> List[unittest.TestResult]:
    """Discovers and runs unit tests for module or modules.

    tests_require: Dependent modules to install with `pip install` before
    running tests. These are modules that are used for testing but are not
    needed in production.

    pattern: Mask for the names of the python files that contain the tests.

    start_dir: Directory with the module, that contain all the TestCases.
    Can also be a list of module directories. In that case each module will
    be scanned separately.

    By default, `start_dir` is None. None value will lead to scanning
    `top_level_dir` for the modules.

    top_level_dir: Top level directory of project (defaults to current
    directory). None will set it to the directory containing the currently
    tested module.

    buffer: Buffer stdout and stderr during tests.

    failfast: Stop on first fail or error.

    verbosity: 0 for quiet, 2 for verbose.
    """

    def rel_to_top(p: Path) -> str:
        return str(
            p.absolute().relative_to(Path(top_level_directory).absolute()))

    try:
        if tests_require:
            install_requirements(tests_require)
            print(splitter)

        if start_directory is not None:
            # todo unittest
            if isinstance(start_directory, str):
                start_dirs = [start_directory]
            else:
                start_dirs = start_directory
        else:
            start_dirs = [str(p) for p in find_start_dirs()]

        results = []

        # skipping directories that do not contain any test cases.
        # It's better to do it now, so terminal output will not end with
        # "module X contains no tests". All messages like this we be
        # at the beginning
        suites: List[Tuple[Path, unittest.TestSuite]] = []

        for sd in start_dirs:
            suite = unittest.TestLoader().discover(
                top_level_dir=(top_level_directory
                               if top_level_directory is not None else sd),
                start_dir=sd,
                pattern=pattern)
            if suite.countTestCases() <= 0:
                print(f'Module "{rel_to_top(Path(sd))}" contains no test cases')
                continue
            suites.append((Path(sd), suite))

        for module_dir, suite in suites:
            print(splitter)
            print(f'Testing module "{rel_to_top(Path(module_dir))}"')

            result = unittest.TextTestRunner(buffer=buffer,
                                             verbosity=verbosity.value,
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
        else:
            raise

    # alternatively we could run the tests exactly as '-m unittest' does
    # with unittest.TestProgram(module=None, argv)
    # where argv is ['python -m unittest', 'discover', ...]


def print_version():
    print(f'neatest {neatest.constants.__version__}')
    print(f'{neatest.constants.__copyright__}')


def main_entry_point():
    if "--version" in sys.argv:
        print_version()
        exit(0)
    run()
