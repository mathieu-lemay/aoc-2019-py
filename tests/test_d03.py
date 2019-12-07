from unittest import TestCase

from aoc.d03 import WireTracer


class D03Test(TestCase):
    def test_get_closest_distance(self):
        params = (
            ("R8,U5,L5,D3", "U7,R6,D4,L4", 6),
            ("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83", 159),
            ("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 135),
        )

        for w1, w2, d in params:
            with self.subTest(w1=w1, w2=w2, d=d):
                wt = WireTracer((w1.split(","), w2.split(",")))
                self.assertEqual(d, wt.get_closest_distance())

    def test_get_fewest_steps(self):
        params = (
            ("R8,U5,L5,D3", "U7,R6,D4,L4", 30),
            ("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83", 610),
            ("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 410),
        )

        for w1, w2, d in params:
            with self.subTest(w1=w1, w2=w2, d=d):
                wt = WireTracer((w1.split(","), w2.split(",")))
                self.assertEqual(d, wt.get_fewest_steps())
