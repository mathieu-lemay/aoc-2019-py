#! /usr/bin/env python

from aoc.intcode import IntCodeRunner


def get_diagnostic_code(program, system_id):
    r = IntCodeRunner(program)
    r.run((system_id,))

    return r.pop_outputs()[-1]


def main():
    with open("input/d05.txt") as f:
        program = f.read()

    print(f"Part 1: {get_diagnostic_code(program, 1)}")
    print(f"Part 2: {get_diagnostic_code(program, 5)}")


if __name__ == "__main__":
    from time import time as ts

    _t = ts()
    main()
    _t = ts() - _t

    print(f"Took {_t:.3f}s")
