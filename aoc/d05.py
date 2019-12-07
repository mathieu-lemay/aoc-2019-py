#! /usr/bin/env python

import os

_debug = os.getenv("DEBUG", "") != ""


def dbgprint(*args, **kwargs):
    if not _debug:
        return

    print(*args, **kwargs)


class IntCodeRunner:
    def __init__(self, intcodes, inputs=None):
        self._intcodes = intcodes
        self._inputs = iter(inputs or [])
        self._ip = 0

    def run(self):
        while True:
            dbgprint(f"DBG: ip: {self._ip}", end="")
            op = self._next_op()
            op, modes = self._decode_op(op)
            dbgprint(f", op={op}, mode={modes}", end="")
            modes = iter(modes)

            if op == 1:
                in1 = self._next_op()
                in2 = self._next_op()
                out = self._next_op()
                dbgprint(f", in1={in1}, in2={in2}, out={out}")

                v1 = self._ld(in1, next(modes, 0))
                v2 = self._ld(in2, next(modes, 0))
                self._st(out, v1 + v2)
            elif op == 2:
                in1 = self._next_op()
                in2 = self._next_op()
                out = self._next_op()
                dbgprint(f", in1={in1}, in2={in2}, out={out}")

                v1 = self._ld(in1, next(modes, 0))
                v2 = self._ld(in2, next(modes, 0))
                self._st(out, v1 * v2)
            elif op == 3:
                out = self._next_op()
                dbgprint(f", out={out}")

                v = self._read()
                self._st(out, v)
            elif op == 4:
                addr = self._next_op()
                dbgprint(f", addr={addr}")

                self._print(addr, next(modes, 0))
            elif op == 5:
                p1 = self._next_op()
                p2 = self._next_op()
                dbgprint(f", p1={p1}, p2={p2}")

                v1 = self._ld(p1, next(modes, 0))
                v2 = self._ld(p2, next(modes, 0))

                if v1 != 0:
                    self._ip = v2
            elif op == 6:
                p1 = self._next_op()
                p2 = self._next_op()
                dbgprint(f", p1={p1}, p2={p2}")

                v1 = self._ld(p1, next(modes, 0))
                v2 = self._ld(p2, next(modes, 0))

                if v1 == 0:
                    self._ip = v2
            elif op == 7:
                p1 = self._next_op()
                p2 = self._next_op()
                out = self._next_op()
                dbgprint(f", p1={p1}, p2={p2}, out={out}")

                v1 = self._ld(p1, next(modes, 0))
                v2 = self._ld(p2, next(modes, 0))

                if v1 < v2:
                    self._st(out, 1)
                else:
                    self._st(out, 0)
            elif op == 8:
                p1 = self._next_op()
                p2 = self._next_op()
                out = self._next_op()
                dbgprint(f", p1={p1}, p2={p2}, out={out}")

                v1 = self._ld(p1, next(modes, 0))
                v2 = self._ld(p2, next(modes, 0))

                if v1 == v2:
                    self._st(out, 1)
                else:
                    self._st(out, 0)
            elif op == 99:
                dbgprint(", exiting")
                break
            else:
                dbgprint(", ERROR")
                dbgprint(self._intcodes)
                raise ValueError(f"Unsupported op: {op}")

        return self._ld(0, 0)

    def _next_op(self):
        op = self._intcodes[self._ip]
        self._ip += 1
        return op

    @staticmethod
    def _decode_op(op):
        opcode = op % 100
        modes = []

        op //= 100

        while op > 0:
            modes.append(op % 10)
            op //= 10

        return opcode, modes

    def _ld(self, addr, mode):
        dbgprint(f"LD: addr={addr}, mode={mode}")
        if mode == 0:
            return self._intcodes[addr]
        elif mode == 1:
            return addr
        else:
            raise ValueError(f"Unsupported mode: {mode}")

    def _st(self, addr, v):
        dbgprint(f"ST: addr={addr}, v={v}")
        self._intcodes[addr] = v

    def _read(self):
        v = next(self._inputs, None)
        if v is None:
            v = int(input(">>> "))

        return v

    def _print(self, addr, mode):
        print(f"<<< {self._ld(addr, mode)}")


def main():
    with open("input/d05.txt") as f:
        values = [int(i) for i in f.read().split(",")]

    print("=== Part 1 ===")
    runner = IntCodeRunner(values[:], inputs=(1,))
    runner.run()
    print("=== Part 1 ===\n")

    print("=== Part 2 ===")
    runner = IntCodeRunner(values[:], inputs=(5,))
    runner.run()
    print("=== Part 2 ===\n")


if __name__ == "__main__":
    from time import time as ts

    _t = ts()
    main()
    _t = ts() - _t

    print(f"Took {_t:.3f}s")
