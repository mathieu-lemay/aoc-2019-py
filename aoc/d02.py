#! /usr/bin/env python

from aoc.intcode import IntCodeCPU
from aoc.utils import load_input


def get_program_output(program, n=None, v=None):
    program = [int(i) for i in program.split(",")]
    if n is not None:
        program[1] = n
    if v is not None:
        program[2] = v

    icr = IntCodeCPU(program)
    icr.run()

    return icr.poke(0)


def get_input_for_output(program, expected_output):
    for n in range(100):
        for v in range(100):
            if get_program_output(program, n, v) == expected_output:
                return 100 * n + v

    raise Exception("Expected output not found")


def main():
    program = load_input("d02.txt")

    print(f"Part 1: {get_program_output(program, 12, 2)}")
    print(f"Part 2: {get_input_for_output(program, 19690720)}")


if __name__ == "__main__":
    from time import time as ts

    _t = ts()
    main()
    _t = ts() - _t

    print(f"Took {_t:.3f}s")
