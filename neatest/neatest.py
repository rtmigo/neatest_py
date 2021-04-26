# SPDX-FileCopyrightText: (c) 2021 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

import argparse
from json import dumps
import subprocess
import io
import sys
from enum import Enum, IntEnum
from typing import List, Optional, Union, Tuple
import unittest
from pathlib import Path
import neatest.constants
from unittest import TextTestRunner, TestSuite, TestLoader, TestResult


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

    if (start_from / "__init__.py").exists():
        return [start_from]

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


default_pattern = '*.py'
default_top_level_dir = '.'
default_start_directory = None
default_verbosity = Verbosity.normal


def run(
        tests_require: Optional[List[str]] = None,
        pattern: str = default_pattern,
        start_directory: Optional[
            Union[str, List[str]]] = default_start_directory,
        top_level_directory: Optional[str] = default_top_level_dir,
        buffer=False,
        failfast=False,
        verbosity=default_verbosity,
        exit_if_failed=True,
        warnings: Warnings = Warnings.default,
        json=False,
) -> unittest.TestResult:
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

    result: Optional[TestResult] = None

    if json:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()

    try:

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

            # skipping directories that do not contain any test cases.
            # It's better to do it now, so terminal output will not end with
            # "module X contains no tests". All messages like this we be
            # at the beginning
            suites: List[unittest.TestSuite] = []

            for sd in start_dirs:
                suite = TestLoader().discover(
                    top_level_dir=(top_level_directory
                                   if top_level_directory is not None else sd),
                    start_dir=sd,
                    pattern=pattern)
                print(
                    f'Module "{rel_to_top(Path(sd))}" contains '
                    f'{suite.countTestCases()} tests')
                if suite.countTestCases() > 0:
                    suites.append(suite)

            combo_suite = TestSuite(suites)

            result = TextTestRunner(buffer=buffer,
                                    verbosity=verbosity.value,
                                    failfast=failfast,
                                    warnings=warnings.value).run(combo_suite)

            if exit_if_failed and not result.wasSuccessful():
                raise TestsError
            return result

        except NeatestError as e:
            print(e.message)
            if exit_if_failed:
                sys.exit(1)
            else:
                raise

        # alternatively we could run the tests exactly as '-m unittest' does
        # with unittest.TestProgram(module=None, argv)
        # where argv is ['python -m unittest', 'discover', ...]
    finally:
        if json:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

            if result:
                print(dumps({
                    'run': result.testsRun,
                    'skipped': len(result.skipped),
                    'failures': len(result.failures),
                    'errors': len(result.errors),
                    'unexpected_successes': len(result.unexpectedSuccesses),
                }))


def print_version():
    print(f'neatest {neatest.constants.__version__}')
    print(f'{neatest.constants.__copyright__}')


class FromUnittestMain:
    @staticmethod
    def convert_select_pattern(pattern):
        if not '*' in pattern:
            pattern = '*%s*' % pattern
        return pattern


def main_entry_point():
    if "--version" in sys.argv:
        print_version()
        exit(0)

    parser = argparse.ArgumentParser()

    # parser.epilog = ('For test discovery all test modules must be '
    #                  'importable from the top level directory of the '
    #                  'project.')

    parser.add_argument('-t', '--top-level-directory', dest='top',
                        default=default_top_level_dir,
                        help=f"Top level directory of project "
                             f"('{default_top_level_dir}' default). All test "
                             f"modules must be importable from this directory")

    parser.add_argument('-s', '--start-directory', dest='start',
                        default=default_start_directory,
                        help="Directory with a package containing the tests. "
                             "If not specified, it will be found automatically "
                             "inside the top-level-directory")
    parser.add_argument('-p', '--pattern', dest='pattern',
                        default=default_pattern,
                        help="Pattern for filenames containing the "
                             f"tests ('{default_pattern}' default)")

    parser.add_argument('-v', '--verbose', dest='verbosity',
                        action='store_const', const=2,
                        help='Verbose output')
    parser.add_argument('-q', '--quiet', dest='verbosity',
                        action='store_const', const=0,
                        help='Quiet output')
    # parser.add_argument('--locals', dest='tb_locals',
    #                     action='store_true',
    #                     help='Show local variables in tracebacks')
    #
    parser.add_argument('-f', '--failfast', dest='failfast',
                        action='store_true',
                        help='Stop on first fail or error')

    # parser.add_argument('-c', '--catch', dest='catchbreak',
    #                     action='store_true',
    #                     help='Catch Ctrl-C and display results so far')

    parser.add_argument('-b', '--buffer', dest='buffer',
                        action='store_true',
                        help='Buffer stdout and stderr during tests')

    parser.add_argument('--json', dest='json',
                        action='store_true',
                        default=False,
                        help='Print only brief statistics in JSON format')

    # parser.add_argument('-k', dest='testNamePatterns',
    #                     action='append',
    #                     type=FromUnittestMain.convert_select_pattern,
    #                     help='Only run tests which match the given substring')

    args = parser.parse_args()

    run(top_level_directory=args.top,
        start_directory=args.start,
        pattern=args.pattern,
        verbosity=Verbosity(args.verbosity or default_verbosity),
        buffer=args.buffer,
        failfast=args.failfast,
        json=args.json)
