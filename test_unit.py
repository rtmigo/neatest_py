from pathlib import Path
import unittest
import neatest
from neatest.neatest import ModulesNotFoundError


class TestMyTest(unittest.TestCase):
    def test_find_start_dirs(self):
        def names(s):
            start = Path('.') / 'sample_projects' / s
            return [p.name for p in neatest.neatest.find_start_dirs(start)]

        self.assertEqual(names('a_b'), ['a', 'b'])
        self.assertEqual(names('b_in_a'), ['a'])
        self.assertEqual(names('only_c'), ['c'])
        with self.assertRaises(ModulesNotFoundError):
            names('complicated')

    def test_run(self):
        # we will also find a low of modules in sample_projects, but there
        # are no TestCases in them, so it will be "Ran 0 tests in 0.000s"

        caught = False
        try:
            neatest.run()  # at least one test fails
        except SystemExit:
            caught = True
        assert caught

        assert sum(r.testsRun for r in neatest.run(exit_if_failed=False)) == 7
        assert sum(r.testsRun for r in neatest.run(exit_if_failed=False)) == 7
        assert sum(r.testsRun for r in neatest.run(pattern="test_*.py")) == 5
        assert sum(r.testsRun for r in neatest.run(pattern="test_*.py")) == 5


if __name__ == "__main__":
    unittest.main()
