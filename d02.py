#! /usr/bin/env python

import math


def run_opcodes(values, n=12, v=2):
    ip = 0

    values[1] = n
    values[2] = v

    while True:
        op = values[ip]
        if op == 1:
            values[values[ip + 3]] = values[values[ip + 1]] + values[values[ip + 2]]
            ip += 4
        elif op == 2:
            values[values[ip + 3]] = values[values[ip + 1]] * values[values[ip + 2]]
            ip += 4
        elif op == 99:
            return values[0]


def main():
    with open("input/d02.txt") as f:
        values = [int(i) for i in f.read().split(",")]

    print(f"Part 1: {run_opcodes(values[:])}")

    input2 = 19690720
    for n in range(100):
        for v in range(100):
            if run_opcodes(values[:], n, v) == input2:
                pt2 = 100 * n + v
                break

    print(f"Part 2: {pt2}")


if __name__ == "__main__":
    from time import time as ts

    _t = ts()
    main()
    _t = ts() - _t

    print(f"Took {_t:.3f}s")
