#!/usr/bin/env python3
"""
Test the match class.

"""
import unittest

try:
    import modules.match as match
except ModuleNotFoundError:
    import sys
    sys.path.append('../..')
    import modules.match as match

class TestMatch(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        """Test the init of the game class

        """
        for size in [9, 13, 19]:
            match_class = match.GoMatch(boardsize=size)
            self.assertIsInstance(match_class, match.GoMatch)

        with self.assertRaises(ValueError):
            match_class = match.GoMatch(boardsize=1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
