#! /usr/bin/env python


def is_valid(digits):
    return digits == sorted(digits) and any(digits.count(i) > 1 for i in set(digits))


def contains_one_pair(digits):
    return 2 in {digits.count(i) for i in set(digits)}


def main():
    a = 273025
    b = 767253

    p1 = p2 = 0

    for i in range(a, b + 1):
        digits = list(str(i))
        if is_valid(digits):
            p1 += 1

            if contains_one_pair(digits):
                p2 += 1

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    from time import time as ts

    _t = ts()
    main()
    _t = ts() - _t

    print(f"Took {_t:.3f}s")
