from pathlib import Path

import neatest


def run():
    # we will also find a low of modules in sample_projects, but there
    # are no TestCases in them, so it will be "Ran 0 tests in 0.000s"
    assert sum(r.testsRun for r in neatest.run()) == 7
    assert sum(r.testsRun for r in neatest.run()) == 7
    assert sum(r.testsRun for r in neatest.run(pattern="test_*.py")) == 5
    assert sum(r.testsRun for r in neatest.run(pattern="test_*.py")) == 5


def test_iter_dir():
    def names(s):
        start = Path('.') / 'sample_projects' / s
        return [p.name for p in neatest.find_start_dir(start)]

    assert names('a_b') == ['a', 'b']
    assert names('b_in_a') == ['a']
    assert names('only_c') == ['c']
    assert names('complicated') == ['b', 'e']


if __name__ == "__main__":
    run()
    test_iter_dir()
    print("ok")
