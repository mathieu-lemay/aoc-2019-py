from unittest import TestCase

from aoc.d06 import get_number_of_transfers, get_orbits


class D06Tests(TestCase):
    def test_get_orbits(self):
        in_ = """COM)B,B)C,C)D,D)E,E)F,B)G,G)H,D)I,E)J,J)K,K)L"""
        in_ = in_.split(",")
        self.assertEqual(42, get_orbits(in_))

    def test_get_number_of_transfers(self):
        in_ = """COM)B,B)C,C)D,D)E,E)F,B)G,G)H,D)I,E)J,J)K,K)L,K)YOU,I)SAN"""

        in_ = in_.split(",")
        self.assertEqual(4, get_number_of_transfers(in_))
