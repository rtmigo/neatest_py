from pathlib import Path

import neatest


def test_run():
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


def test_find_start_dirs():
    def names(s):
        start = Path('.') / 'sample_projects' / s
        return [p.name for p in neatest.find_start_dirs(start)]

    assert names('a_b') == ['a', 'b']
    assert names('b_in_a') == ['a']
    assert names('only_c') == ['c']
    assert names('complicated') == ['b', 'e']


if __name__ == "__main__":
    try:
        test_run()
        test_find_start_dirs()
        print("NEATEST OK")
    except:
        # the following message indicates a problem in neatest itself
        print("NEATEST ERROR")
