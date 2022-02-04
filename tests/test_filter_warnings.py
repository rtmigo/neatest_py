import unittest

from neatest._neatest import _remove_those_contain


class Test(unittest.TestCase):
    def test(self):
        messages = ['Warning Alpha', 'Warning Beta', 'Warning Gamma']
        with self.subTest('None'):
            self.assertEqual(
                _remove_those_contain(messages, None),
                messages)
        with self.subTest('Empty'):
            self.assertEqual(
                _remove_those_contain(messages, []),
                messages)
        with self.subTest('No matches'):
            self.assertEqual(
                _remove_those_contain(messages, ['labuda']),
                messages)
        with self.subTest('removing one warning'):
            self.assertEqual(
                _remove_those_contain(messages, ['Beta']),
                ['Warning Alpha', 'Warning Gamma'])

        with self.subTest('removing two warnings'):
            self.assertEqual(
                _remove_those_contain(messages, ['Gamma', 'Alpha']),
                ['Warning Beta'])
