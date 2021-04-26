import subprocess
import sys, os
from pathlib import Path
import unittest
from typing import List, Optional
import json

import neatest
from neatest.neatest import ModulesNotFoundError


def _run(add_args: List[str] = None, cwd: Optional[Path] = None):
    env = os.environ.copy()
    package_dir = Path(__file__).parent.parent
    env['PYTHONPATH'] = str(package_dir) + ':' + env.get('PYTHONPATH', '')

    res = subprocess.run(
        [sys.executable, '-m', 'neatest'] + (add_args or []),
        env=env,
        cwd=str(cwd) if cwd else None,
        capture_output=True, encoding="utf-8")
    return res


def sample_project_path(s: str) -> Path:
    return Path(__file__).parent.parent / 'tests_sample_projects' / s


class TestsProcess(unittest.TestCase):

    def test_version(self):
        completed = _run(['--version'])
        self.assertTrue(completed.stdout.startswith('neatest'))

    def test_help(self):
        completed = _run(['--help'])
        self.assertTrue("usage:" in completed.stdout)

    def test_pattern(self):
        completed = _run(["--json"], cwd=sample_project_path('tests'))
        d = json.loads(completed.stdout)
        self.assertEqual(d['run'], 7)

        completed = _run(["-p", "test_*.py", "--json"],
                         cwd=sample_project_path('tests'))
        d = json.loads(completed.stdout)
        self.assertEqual(d['run'], 5)


class TestMyTest(unittest.TestCase):

    def test_find_start_dirs(self):
        def names(s):
            start = sample_project_path(s)
            return [p.name for p in neatest.neatest.find_start_dirs(start)]

        self.assertEqual(names('a_b'), ['a', 'b'])
        self.assertEqual(names('b_in_a'), ['a'])
        self.assertEqual(names('only_c'), ['c'])
        self.assertEqual(names('flat'), ['flat'])
        self.assertEqual(names('with_invisible'), ['find_me'])

        with self.assertRaises(ModulesNotFoundError):
            names('complicated')


if __name__ == "__main__":
    unittest.main()

    # TestMyTest().test_version()
    # z = unittest.main(buffer=False, exit=False)
    # print(f"NEATEST OK: {z.result.wasSuccessful()}")
