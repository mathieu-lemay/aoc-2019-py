from unittest import TestCase

from d01 import get_fuel_req, get_fuel_req_recur


class D01Test(TestCase):
    def test_get_fuel_req(self):
        params = (
            (12, 2),
            (14, 2),
            (1969, 654),
            (100756, 33583),
        )

        for w, f in params:
            with self.subTest(w=w, f=f):
                self.assertEqual(f, get_fuel_req(w))

    def test_get_fuel_req_recur(self):
        params = (
            (12, 2),
            (14, 2),
            (1969, 966),
            (100756, 50346),
        )

        for w, f in params:
            with self.subTest(w=w, f=f):
                self.assertEqual(f, get_fuel_req_recur(w))
