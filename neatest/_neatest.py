# SPDX-FileCopyrightText: (c) 2021 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

import argparse
import io
import subprocess
import sys
import unittest
import warnings as wrn
from enum import Enum, IntEnum
from json import dumps
from pathlib import Path
from typing import List, Optional, Union, NamedTuple
from unittest import TextTestRunner, TestSuite, TestLoader, TestResult

import neatest._constants


class NeatestError(Exception):
    def __init__(self, message: str):
        self.message = message


class InstallationError(NeatestError):
    def __init__(self):
        super().__init__("Failed to install test dependencies.")


class TestsError(NeatestError):
    def __init__(self):
        super().__init__("Testing failed.")


class WarningsError(NeatestError):
    def __init__(self):
        super().__init__("Testing failed due to warnings.")


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


class PythonWarningsArgs(Enum):
    # https://www.geeksforgeeks.org/warnings-in-python/
    default = "default"
    error = "error"
    ignore = "ignore"
    always = "always"
    module = "module"
    once = "once"


class Warnings(Enum):
    ignore = "ignore"
    print = "print"
    fail = "fail"


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
default_warnings_handling = Warnings.print


class RunResult(NamedTuple):
    tests: TestResult
    warnings: List[wrn.WarningMessage]


def set_warnings_filter(w: PythonWarningsArgs):
    # the same as TextTestRunner.run in Python 3.9.
    # Comments are preserved
    if w is not None:
        # if self.warnings is set, use it to filter all the warnings
        wrn.simplefilter(w.value)
        # if the filter is 'default' or 'always', special-case the
        # warnings from the deprecated unittest methods to show them
        # no more than once per module, because they can be fairly
        # noisy.  The -Wd and -Wa flags can be used to bypass this
        # only when self.warnings is None.
        if w in [PythonWarningsArgs.default, PythonWarningsArgs.always]:
            wrn.filterwarnings(
                'module',
                category=DeprecationWarning,
                message=r'Please use assert\w+ instead.')


class TempMute:
    def __init__(self):
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()

    def unmute(self):
        if self.old_stdout is not None:
            sys.stdout = self.old_stdout
            sys.stderr = self.old_stderr
            self.old_stdout = None
            self.old_stderr = None


def run(
        tests_require: Optional[List[str]] = None,
        start_directory: Optional[
            Union[str, List[str]]] = default_start_directory,
        buffer=False,
        failfast=False,
        verbosity=default_verbosity,
        exit_if_failed=True,
        warnings: Warnings = default_warnings_handling,
        json=False,
) -> RunResult:
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

    top_level_directory = default_top_level_dir
    pattern = default_pattern

    temp_mute = TempMute() if json else None

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

            suites: List[unittest.TestSuite] = []

            for sd in start_dirs:
                suite = TestLoader().discover(
                    top_level_dir=(top_level_directory
                                   if top_level_directory is not None else sd),
                    start_dir=sd,
                    pattern=pattern)
                print(
                    f'Package "{rel_to_top(Path(sd))}" contains '
                    f'{suite.countTestCases()} tests')
                if suite.countTestCases() > 0:
                    suites.append(suite)

            combo_suite = TestSuite(suites)

            with wrn.catch_warnings(record=True) as catcher:

                # with the default unittest, even if warnings are enabled, the
                # --buffer argument makes them invisible: warnings are
                # printed, but the output is buffered and not shown not
                # displayed unless the corresponding test fails
                #
                # But we want to see the warnings, even with --buffered,
                # until they are explicitly disabled.
                #
                # So the run(warning=None), and we handle all the warnings
                # manually

                set_warnings_filter(
                    PythonWarningsArgs.ignore
                    if warnings == Warnings.ignore
                    else PythonWarningsArgs.default)

                result = TextTestRunner(buffer=buffer,
                                        verbosity=verbosity.value,
                                        failfast=failfast,
                                        warnings=None).run(combo_suite)

                caught_warnings = list(catcher)

            if caught_warnings:
                print()
                print(splitter)
                print(f"Caught {len(caught_warnings)} warnings:")
                for w in caught_warnings:
                    print()
                    print(wrn.formatwarning(message=w.message,
                                            category=w.category,
                                            filename=w.filename,
                                            lineno=w.lineno,
                                            line=w.line))

            if json:
                assert temp_mute is not None
                temp_mute.unmute()

                print(dumps({
                    'run': result.testsRun,
                    'skipped': len(result.skipped),
                    'failures': len(result.failures),
                    'errors': len(result.errors),
                    'unexpected_successes': len(result.unexpectedSuccesses),
                    'warnings': len(caught_warnings) if caught_warnings else 0
                }))

            if exit_if_failed:
                if not result.wasSuccessful():
                    raise TestsError
                if warnings == Warnings.fail and caught_warnings:
                    raise WarningsError

            return RunResult(result, caught_warnings)

        except NeatestError as e:
            if not json:
                print(e.message)
            if exit_if_failed:
                sys.exit(1)
            else:
                raise

        # alternatively we could run the tests exactly as '-m unittest' does
        # with unittest.TestProgram(module=None, argv)
        # where argv is ['python -m unittest', 'discover', ...]
    finally:
        if temp_mute:
            temp_mute.unmute()


def print_version():
    print(f'neatest {neatest._constants.__version__}')
    print(f'{neatest._constants.__copyright__}')


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

    parser.add_argument('-s', '--start-directory', dest='start',
                        default=default_start_directory,
                        help="Directory with a package containing the tests. "
                             "If not specified, the packages will be found "
                             "automatically inside the current directory")

    parser.add_argument('-r', '--require', action='append',
                        help="Packages to be installed with 'pip install' "
                             "before running tests. "
                             "(e.g. '-r requests -r lmxl')")

    group = parser.add_mutually_exclusive_group()
    # group.add_argument("-v", "--verbose", action="store_true")
    # group.add_argument("-q", "--quiet", action="store_true")

    group.add_argument('-v', '--verbose', dest='verbosity',
                       action='store_const', const=2,
                       help='Verbose output')
    group.add_argument('-q', '--quiet', dest='verbosity',
                       action='store_const', const=0,
                       help='Quiet output')
    # parser.add_argument('--locals', dest='tb_locals',
    #                     action='store_true',
    #                     help='Show local variables in tracebacks')
    #
    parser.add_argument('-f', '--failfast', dest='failfast',
                        action='store_true',
                        help='Stop on first fail or error')

    parser.add_argument('--json', dest='json',
                        action='store_true',
                        default=False,
                        # 'Print only brief statistics in JSON format'
                        help=argparse.SUPPRESS)

    parser.add_argument('-w', '--warnings', dest='warnings',
                        choices=[Warnings.print.value,
                                 Warnings.ignore.value,
                                 Warnings.fail.value],
                        default=default_warnings_handling.value,
                        help=f"Way to handle warnings "
                             f"(default: '{default_warnings_handling.value}')")

    parser.add_argument('--version',
                        action='store_true',
                        default=False,
                        help="Show version info and exit")

    # parser.add_argument('-k', dest='testNamePatterns',
    #                     action='append',
    #                     type=FromUnittestMain.convert_select_pattern,
    #                     help='Only run tests which match the given substring')

    args = parser.parse_args()

    run(start_directory=args.start,
        tests_require=args.require,
        verbosity=Verbosity(args.verbosity or default_verbosity),
        buffer=True,
        failfast=args.failfast,
        warnings=Warnings(args.warnings),
        json=args.json)
