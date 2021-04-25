import unittest

class Stub2(unittest.TestCase):
    # we just want to discover this tests and make sure that 2 tests are executed

    def test_1(self):
        open(__file__).read()
        pass

    def test_2(self):
        raise AssertionError
        pass
