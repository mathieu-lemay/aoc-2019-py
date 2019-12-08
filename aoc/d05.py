#! /usr/bin/env python

from aoc.intcode import IntCodeCPU
from aoc.utils import load_input


def get_diagnostic_code(program, system_id):
    r = IntCodeCPU(program)
    r.run((system_id,))

    return r.pop_output()[-1]


def main():
    program = load_input("d05.txt")

    print(f"Part 1: {get_diagnostic_code(program, 1)}")
    print(f"Part 2: {get_diagnostic_code(program, 5)}")


if __name__ == "__main__":
    from time import time as ts

    _t = ts()
    main()
    _t = ts() - _t

    print(f"Took {_t:.3f}s")
