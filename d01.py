#! /usr/bin/env python

import math


def get_fuel_req(weight):
    return weight // 3 - 2


def get_fuel_req_recur(weight):
    f = weight // 3 - 2
    if f <= 0:
        return 0

    return f + get_fuel_req_recur(f)


def main():
    with open("/input/d01.txt") as f:
        values = f.readlines()

    sum_fuel = sum(get_fuel_req(int(l)) for l in values)
    sum_fuel_2 = sum(get_fuel_req_recur(int(l)) for l in values)

    print(f"Part 1: {sum_fuel}")
    print(f"Part 2: {sum_fuel_2}")


if __name__ == "__main__":
    from time import time as ts

    _t = ts()
    main()
    _t = ts() - _t

    print(f"Took {_t:.3f}s")
