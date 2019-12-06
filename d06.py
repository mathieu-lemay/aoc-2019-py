#! /usr/bin/env python

import unittest


def list_parents(m, k):
    p = m.get(k)

    if not p:
        return []

    parents = []
    parents.append(p)

    parents += list_parents(m, p)

    return parents


def get_orbits(input_):
    m = {}
    for i in input_:
        x, y = i.split(")")
        m[y] = x

    return sum(len(list_parents(m, k)) for k in m.keys())


def get_orbits2(input_):
    m = {}
    for i in input_:
        x, y = i.split(")")
        m[y] = x

    you_parents = list_parents(m, "YOU")
    san_parents = list_parents(m, "SAN")

    for p in you_parents:
        if p in set(san_parents):
            return you_parents.index(p) + san_parents.index(p)

    raise Exception()


def main():
    with open("input/d06.txt") as f:
        x = [i.strip() for i in f.readlines()]

    print(f"Part 1: {get_orbits(x)}")
    print(f"Part 1: {get_orbits2(x)}")


class Tests(unittest.TestCase):
    def test_p1(self):
        in_ = """COM)B,B)C,C)D,D)E,E)F,B)G,G)H,D)I,E)J,J)K,K)L"""
        in_ = in_.split(",")
        self.assertEqual(42, get_orbits(in_))

    def test_p2(self):
        in_ = """COM)B,B)C,C)D,D)E,E)F,B)G,G)H,D)I,E)J,J)K,K)L,K)YOU,I)SAN"""

        in_ = in_.split(",")
        self.assertEqual(4, get_orbits2(in_))


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
