from pathlib import Path
import unittest
import neatest
from neatest.neatest import ModulesNotFoundError, Verbosity


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

    def test_start_directory(self):
        neatest.run(start_directory='tests', exit_if_failed=False)

    def test_run(self):

        # open(__file__, "r")

        # we will also find a low of modules in sample_projects, but there
        # are no TestCases in them, so it will be "Ran 0 tests in 0.000s"

        caught = False
        try:
            neatest.run()  # at least one test fails
        except SystemExit:
            caught = True
        assert caught

        assert neatest.run(exit_if_failed=False).testsRun == 7
        assert neatest.run(exit_if_failed=False).testsRun == 7
        assert neatest.run(pattern="test_*.py").testsRun == 5
        assert neatest.run(pattern="test_*.py").testsRun == 5


if __name__ == "__main__":
    z = unittest.main(buffer=False, exit=False)
    print(f"NEATEST OK: {z.result.wasSuccessful()}")
