from unittest import TestCase

from aoc.d16 import fft


class D16Tests(TestCase):
    def test_fft(self):
        test_params = (
            ("12345678", 1, "48226158"),
            ("12345678", 2, "34040438"),
            ("12345678", 3, "03415518"),
            ("12345678", 4, "01029498"),
            ("80871224585914546619083218645595", 100, "24176176"),
            ("19617804207202209144916044189917", 100, "73745418"),
            ("69317163492948606335995924319873", 100, "52432133"),
        )

        for signal, passes, expected in test_params:
            with self.subTest(signal=signal, passes=passes, expected=expected):
                signal = [int(i) for i in list(signal)]
                expected = [int(i) for i in list(expected)]
                res = list(fft(signal, passes)[:8])
                self.assertEqual(expected, res)
