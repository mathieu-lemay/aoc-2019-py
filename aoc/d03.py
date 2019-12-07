#! /usr/bin/env python

import math


class WireTracer:
    def __init__(self, wires):
        self.wires = []
        self.crossing_pts = []

        for w in wires:
            self.wires.append(self._trace_wire(w))

        self.crossing_pts = set(self.wires[0])

        for w in self.wires[1:]:
            self.crossing_pts &= set(w)

        self.crossing_pts -= {(0, 0)}

    def _trace_wire(self, wire_movements):
        positions = []
        x, y = 0, 0

        positions.append((x, y))

        for m in wire_movements:
            d, c = m[0], int(m[1:])

            if d == "U":
                positions += [(x, y + (i + 1)) for i in range(c)]
                x, y = x, y + c
            elif d == "D":
                positions += [(x, y - (i + 1)) for i in range(c)]
                x, y = x, y - c
            elif d == "L":
                positions += [(x - (i + 1), y) for i in range(c)]
                x, y = x - c, y
            elif d == "R":
                positions += [(x + (i + 1), y) for i in range(c)]
                x, y = x + c, y

        return positions

    def get_closest_distance(self):
        return min(abs(p[0]) + abs(p[1]) for p in self.crossing_pts)

    def get_fewest_steps(self):
        return min(sum(w.index(p) for w in self.wires) for p in self.crossing_pts)


def main():
    with open("input/d03.txt") as f:
        wires = [l.split(",") for l in f.readlines()]

    wt = WireTracer(wires)

    print(f"Part 1: {wt.get_closest_distance()}")
    print(f"Part 2: {wt.get_fewest_steps()}")


if __name__ == "__main__":
    from time import time as ts

    _t = ts()
    main()
    _t = ts() - _t

    print(f"Took {_t:.3f}s")
