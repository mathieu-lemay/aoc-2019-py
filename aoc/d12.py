#! /usr/bin/env python
import re
from pprint import pformat

import numpy as np

from aoc.utils import load_input_by_line


class Moon:
    def __init__(self, x, y, z, vx=0, vy=0, vz=0):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz

    @property
    def pos(self):
        return self.x, self.y, self.z

    @property
    def v(self):
        return self.vx, self.vy, self.vz

    @property
    def pot_e(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    @property
    def kin_e(self):
        return abs(self.vx) + abs(self.vy) + abs(self.vz)

    @property
    def e(self):
        return self.pot_e * self.kin_e

    def apply_gravity(self, o, axis):
        if axis & 1:
            if self.x < o.x:
                self.vx += 1
                o.vx -= 1
            elif self.x > o.x:
                self.vx -= 1
                o.vx += 1

        if axis & 2:
            if self.y < o.y:
                self.vy += 1
                o.vy -= 1
            elif self.y > o.y:
                self.vy -= 1
                o.vy += 1

        if axis & 4:
            if self.z < o.z:
                self.vz += 1
                o.vz -= 1
            elif self.z > o.z:
                self.vz -= 1
                o.vz += 1

    def move(self, axis):
        if axis & 1:
            self.x += self.vx
        if axis & 2:
            self.y += self.vy
        if axis & 4:
            self.z += self.vz

    def __eq__(self, o):
        return self.x == o.x and self.y == o.y and self.z == o.z

    def __str__(self):
        return f"<Moon(pos={self.pos}, v={self.v})>"

    def __repr__(self):
        return str(self)


class System:
    def __init__(self, moons: [Moon]):
        self.moons = moons
        self.size = len(moons)

    @property
    def e(self):
        return sum(m.e for m in self.moons)

    def step(self, n=1, axis=7):
        for i in range(n):
            self._step(axis)

    def _step(self, axis):
        self._apply_gravity(axis)
        self._move(axis)

    def _apply_gravity(self, axis):
        for i in range(self.size - 1):
            for j in range(i + 1, self.size):
                m1 = self.moons[i]
                m2 = self.moons[j]
                m1.apply_gravity(m2, axis)

    def _move(self, axis):
        for m in self.moons:
            m.move(axis)

    def get_period(self, axis):
        init = self._get_positions(axis)
        i = 0

        while True:
            i += 1
            self.step(axis=axis)
            if self._get_positions(axis) == init:
                return i * 2

    def _get_positions(self, axis):
        if axis == 1:
            return [m.vx for m in self.moons]

        if axis == 2:
            return [m.vy for m in self.moons]

        if axis == 4:
            return [m.vz for m in self.moons]

    def __eq__(self, o):
        return self.moons == o.moons

    def __str__(self):
        return pformat(self.moons)

    def __repr__(self):
        return str(self)


def create_system(input_values):
    moons = []

    matcher = re.compile(r"<x=(-?[0-9]+), y=(-?[0-9]+), z=(-?[0-9]+)>")

    for l in input_values:
        m = matcher.match(l)
        if not m:
            raise ValueError(l)

        x = int(m.group(1))
        y = int(m.group(2))
        z = int(m.group(3))

        moons.append(Moon(x, y, z))

    return System(moons)


def get_energy_after_steps(system, n=1):
    system.step(n)
    return system.e


def get_steps_before_repeat(system):
    px = system.get_period(1)
    py = system.get_period(2)
    pz = system.get_period(4)

    # noinspection PyUnresolvedReferences
    return np.lcm.reduce([px, py, pz])


def main():
    input_values = load_input_by_line("d12.txt")

    system = create_system(input_values)
    print(f"Part 1: {get_energy_after_steps(system, 1000)}")

    system = create_system(input_values)
    print(f"Part 2: {get_steps_before_repeat(system)}")


if __name__ == "__main__":
    from time import time as ts

    _t = ts()
    main()
    _t = ts() - _t

    print(f"Runtime: {_t:.3f}s")
