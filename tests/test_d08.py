from unittest import TestCase

from aoc.d07 import get_thruster_output, get_thruster_output_with_feedback
from aoc.d08 import get_layers, merge_layers


class D08Tests(TestCase):
    def test_get_layers(self):
        img_data = "123456789012"
        x, y = 3, 2

        self.assertEqual([[1, 2, 3, 4, 5, 6], [7, 8, 9, 0, 1, 2]], get_layers(img_data, x, y))

    def test_merge_layers(self):
        layers = [[0, 2, 2, 2], [1, 1, 2, 2], [2, 2, 1, 2], [0, 0, 0, 0]]
        self.assertEqual([0, 1, 1, 0], merge_layers(layers))
