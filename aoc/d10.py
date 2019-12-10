#! /usr/bin/env python
import math

from aoc.utils import load_input_by_line


def get_deg(x, y):
    deg = math.degrees(math.atan2(y, x)) + 90
    if deg < 0:
        deg += 360

    return deg


class Asteroid:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.nb_in_sight = 0

    def angle_of(self, a: "Asteroid"):
        return get_deg(a.x - self.x, a.y - self.y)

    def dist(self, a: "Asteroid"):
        return abs(a.x - self.x) + abs(a.y - self.y)

    @property
    def coords(self):
        return self.x, self.y

    def __str__(self):
        return f"Asteroid(x={self.x}, y={self.y}, nb={self.nb_in_sight})"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self.x, self.y))


def get_asteroids(space_map):
    asteroids = []

    for x in range(len(space_map[0])):
        for y in range(len(space_map)):
            if space_map[y][x] == "#":
                asteroids.append(Asteroid(x, y))

    for a1 in asteroids:
        angles = set(a1.angle_of(a2) for a2 in asteroids if a1 is not a2)
        a1.nb_in_sight = len(angles)

    return asteroids


def get_best_asteroid(asteroids: [Asteroid]) -> Asteroid:
    return sorted(asteroids, key=lambda a: a.nb_in_sight, reverse=True)[0]


def get_next_target(ast_with_coords: (Asteroid, float, int), deg):
    max_deg = max(a[1] for a in ast_with_coords)
    if deg is None or deg > max_deg:
        tgt = next((a for a in ast_with_coords), None)
    else:
        tgt = next((a for a in ast_with_coords if a[1] > deg), None)

    if not tgt:
        raise ValueError("No targets left")

    return tgt


def obliterate(a: Asteroid, asteroids: [Asteroid], n=200) -> Asteroid:
    i = 0
    deg = None
    tgt = None

    asteroids_with_coords = sorted(
        [(i, a.angle_of(i), a.dist(i)) for i in asteroids if i is not a], key=lambda awc: (awc[1], awc[2])
    )

    # from pprint import pprint
    # pprint(asteroids_with_coords)

    while i < n:
        x = get_next_target(asteroids_with_coords, deg)
        asteroids_with_coords.remove(x)
        tgt = x[0]
        deg = x[1]
        i += 1

    return tgt


def main():
    space_map = [list(l) for l in load_input_by_line("d10.txt")]
    asteroids = get_asteroids(space_map)

    best = get_best_asteroid(asteroids)
    print(f"Part 1: {best.nb_in_sight}")

    tgt = obliterate(best, asteroids)
    print(f"Part 2: {tgt.x * 100 + tgt.y}")


if __name__ == "__main__":
    from time import time as ts

    _t = ts()
    main()
    _t = ts() - _t

    print(f"Runtime: {_t:.3f}s")
