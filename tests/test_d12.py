from unittest import TestCase

from aoc.d12 import Moon, System, create_system, get_energy_after_steps, get_steps_before_repeat


def parse_map(map_str):
    return [list(l) for l in map_str.split("\n")]


class D12Tests(TestCase):
    def setUp(self) -> None:
        self.s1 = System([Moon(-1, 0, 2), Moon(2, -10, -7), Moon(4, -8, 8), Moon(3, 5, -1)])
        self.s2 = System([Moon(-8, -10, 0), Moon(5, 5, 10), Moon(2, -7, 3), Moon(9, -8, -3)])

    def test_create_system(self):
        input_values = (
            "<x=-1, y=0, z=2>",
            "<x=2, y=-10, z=-7>",
            "<x=4, y=-8, z=8>",
            "<x=3, y=5, z=-1>",
        )

        self.assertEqual(self.s1, create_system(input_values))

    def test_step(self):
        system = System([Moon(-1, 0, 2), Moon(2, -10, -7), Moon(4, -8, 8), Moon(3, 5, -1),])

        system.step(10)

        expected = System(
            [Moon(2, 1, -3, -3, -1, 1), Moon(1, -8, 0, -1, 1, 3), Moon(3, -6, 1, 3, 2, -3), Moon(2, 0, 4, 1, -1, -1),]
        )

        self.assertEqual(expected, system)
        self.assertEqual(179, system.e)

    def test_get_energy_after_steps(self):
        params = (
            (self.s1, 10, 179),
            (self.s2, 100, 1940),
        )
        for system, steps, e in params:
            with self.subTest():
                self.assertEqual(e, get_energy_after_steps(system, steps))

    def test_get_steps_before_repeat(self):
        params = (
            (self.s1, 2772),
            (self.s2, 4686774924),
        )

        for system, steps in params:
            with self.subTest():
                self.assertEqual(steps, get_steps_before_repeat(system))
