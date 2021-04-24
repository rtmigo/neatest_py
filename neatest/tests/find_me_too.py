import unittest
import tempfile

class Stub2(unittest.TestCase):
    # we just want to discover this test and make sure that 2 tests are executed

    def test_1(self):

        #ntf = tempfile.NamedTemporaryFile()
        #open('/tmp/x', 'w')
        pass

    def test_2(self):
        pass
