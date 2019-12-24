from unittest import TestCase

from aoc.d24 import parse_input, render, tick


class D16Tests(TestCase):
    def test_parse_input(self):
        test_params = (
            (".....\n.....\n.....\n.....\n.....", 0),
            ("#####\n#####\n#####\n#####\n#####", 0b1111111111111111111111111),
            ("#....\n.....\n.....\n.....\n.....", 1),
            (".....\n.....\n.....\n.....\n....#", 0b1000000000000000000000000),
            ("....#\n....#\n....#\n....#\n....#", 0b1000010000100001000010000),
        )

        for in_, expected in test_params:
            with self.subTest(in_=in_, expected=expected):
                self.assertEqual(expected, parse_input(in_))

    def test_tick(self):
        test_params = (
            (0b0000100100110010100110000, 0b0011011011101110111101001),
            (0b0011011011101110111101001, 0b1110101000100001000011111),
            (0b1110101000100001000011111, 0b1011001101110000111100001),
            (0b1011001101110000111100001, 0b0001100000100111000001111),
        )

        for state, expected in test_params:
            with self.subTest(a=state, b=expected):
                self.assertEqual(expected, tick(state))
