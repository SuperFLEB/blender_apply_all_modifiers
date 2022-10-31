from . import pkg

__package__ = pkg()

import unittest


class DummyTestCase(unittest.TestCase):

    def dummy_test(self):
        """A test"""
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
