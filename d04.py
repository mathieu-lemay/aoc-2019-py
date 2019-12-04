#! /usr/bin/env python

import unittest


def is_valid(digits):
    return digits == sorted(digits) and any(digits.count(i) > 1 for i in set(digits))


def contains_one_pair(digits):
    return 2 in {digits.count(i) for i in set(digits)}


def main():
    a = 273025
    b = 767253

    p1 = p2 = 0

    for i in range(a, b + 1):
        digits = list(str(i))
        if is_valid(digits):
            p1 += 1

            if contains_one_pair(digits):
                p2 += 1

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


class Tests(unittest.TestCase):
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


def tests():
    suite = unittest.makeSuite(Tests)
    unittest.TextTestRunner().run(suite)
    print("\n----------------------------------------------------------------------\n")


if __name__ == "__main__":
    from time import time as ts

    tests()

    _t = ts()
    main()
    _t = ts() - _t

    print(f"Took {_t:.3f}s")
