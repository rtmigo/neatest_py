import neatest

if __name__ == "__main__":
    assert neatest.run().testsRun == 5
    assert neatest.run().testsRun == 5
    neatest.pattern = "*.py"
    assert neatest.run().testsRun == 7
