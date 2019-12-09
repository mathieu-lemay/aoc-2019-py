#! /usr/bin/env python

from time import time as ts

from aoc.intcode import IntCodeCPU
from aoc.utils import load_input


def get_boost_keycode(program):
    cpu = IntCodeCPU(program)
    cpu.run((1,))
    output = cpu.pop_output()
    assert len(output) == 1
    return output[0]


def get_coords(program):
    cpu = IntCodeCPU(program)
    cpu.run((2,))
    output = cpu.pop_output()
    assert len(output) == 1
    return output[0]


def main():
    program = load_input("d09.txt")

    _t = ts()
    p1 = get_boost_keycode(program)
    _t = ts() - _t
    print(f"Part 1: {p1} ({_t:.3f}s)")

    _t = ts()
    p2 = get_coords(program)
    _t = ts() - _t
    print(f"Part 2: {p2} ({_t:.3f}s)")


if __name__ == "__main__":
    main()
