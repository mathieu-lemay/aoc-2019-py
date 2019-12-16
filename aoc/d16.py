#! /usr/bin/env python
from time import time as ts

from aoc.utils import load_input


def fft(signal, passes):
    siglen = len(signal)

    for _ in range(passes):
        output = []
        for out_idx in range(siglen):
            res = 0
            i = out_idx
            psize = out_idx + 1
            while i < siglen:
                res += sum(signal[i : i + psize])
                i += psize * 2
                res -= sum(signal[i : i + psize])
                i += psize * 2

            output.append(abs(res) % 10)

        signal = output

    return signal


def fft2(signal, passes):
    siglen = len(signal)

    for _ in range(passes):
        output = [0] * siglen
        res = 0
        for out_idx in range(siglen):
            i = siglen - out_idx - 1

            res += signal[i]

            output[i] = abs(res) % 10

        signal = output

    return signal


def main():
    signal = [int(i) for i in list(load_input("d16.txt"))]

    _t = ts()
    output = fft(signal, 100)
    _t = ts() - _t
    p1 = "".join([str(c) for c in output[:8]])
    print(f"Part 1: {p1}")
    print(f"Runtime: {_t:.3f}s")

    offset = int("".join([str(c) for c in signal[:7]]))
    signal = (signal * 10000)[offset:]
    _t = ts()
    output = fft2(signal, 100)
    _t = ts() - _t
    p2 = "".join([str(c) for c in output[:8]])
    print(f"Part 2: {p2}")
    print(f"Runtime: {_t:.3f}s")


if __name__ == "__main__":
    main()
