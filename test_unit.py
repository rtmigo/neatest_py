import neatest

if __name__ == "__main__":
    assert neatest.run().testsRun == 7
    assert neatest.run().testsRun == 7
    neatest.pattern = "test_*.py"
    assert neatest.run().testsRun == 5
    assert neatest.run().testsRun == 5


