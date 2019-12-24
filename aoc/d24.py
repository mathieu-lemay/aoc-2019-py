#! /usr/bin/env python
from time import time as ts

from aoc.utils import load_input, split_list


def parse_input(in_):
    val = 0
    in_ = in_.replace("\n", "")

    for i in range(len(in_)):
        if in_[i] == "#":
            val |= 1 << i

    return val


def tick(state):
    ns = 0

    for i in range(25):
        n = 0
        c = (state >> i) & 1

        y, x = divmod(i, 5)
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            nx = x + dx
            ny = y + dy
            if 0 <= nx < 5 and 0 <= ny < 5:
                n += (state >> (ny * 5 + nx)) & 1

        if (c == 1 and n == 1) or (c == 0 and 0 < n < 3):
            ns |= 1 << i

    return ns


def render(state, end="\n"):
    chars = []
    for i in range(25):
        v = state & (1 << i)
        chars.append("#" if v else ".")

    for b in split_list(chars, 5):
        print("".join(b), end=end)


def get_first_repeat_state(state):
    states = set()
    states.add(state)
    state = tick(state)

    while state not in states:
        states.add(state)
        state = tick(state)

    return state


def main():
    in_ = load_input("d24.txt")
    state = parse_input(in_)

    new_state = get_first_repeat_state(state)
    print(f"Part 1: {new_state}")


if __name__ == "__main__":
    _t = ts()
    main()
    _t = ts() - _t

    print(f"Runtime: {_t:.3f}s")
