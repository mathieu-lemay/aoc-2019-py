from unittest import TestCase

from aoc.d04 import contains_one_pair, is_valid


class D04Tests(TestCase):
    def test_is_valid(self):
        params = (
            (111111, True),
            (223450, False),
        )

        for i, expected in params:
            with self.subTest(i=i, expected=expected):
                self.assertEqual(is_valid(list(str(i))), expected)

    def test_contains_one_pair(self):
        params = (
            (112233, True),
            (123444, False),
            (111122, True),
        )
        for i, expected in params:
            with self.subTest(i=i, expected=expected):
                self.assertEqual(contains_one_pair(list(str(i))), expected)
