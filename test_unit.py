from pathlib import Path

import neatest


def run():
    assert neatest.run().testsRun == 7
    assert neatest.run().testsRun == 7
    neatest.pattern = "test_*.py"
    assert neatest.run().testsRun == 5
    assert neatest.run().testsRun == 5


def test_iter_dir():
    def proj(s):
        return Path('.') / 'sample_projects' / s

    assert neatest.find_start_dir(
        proj('b_in_a')).name == "a"

    assert neatest.find_start_dir(
        proj('only_c')).name == "c"

    caught = False
    try:
        neatest.find_start_dir(proj('a_b'))
    except neatest.NeatestMoreThanOneModuleError:
        caught = True
    assert caught


if __name__ == "__main__":
    run()
    test_iter_dir()
