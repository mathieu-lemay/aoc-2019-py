#! /usr/bin/env python

import os
from enum import IntEnum

_debug = os.getenv("DEBUG", "") != ""


def dbgprint(*args, **kwargs):
    if not _debug:
        return

    print(*args, **kwargs)


class Op(IntEnum):
    ADD = 1
    MUL = 2
    READ = 3
    WRITE = 4
    BNE = 5
    BEQ = 6
    LT = 7
    EQ = 8
    HALT = 99


class IntCodeCPU:
    def __init__(self, program, id_=0):
        if isinstance(program, str):
            self._intcodes = [int(i) for i in program.split(",")]
        else:
            self._intcodes = program
        self._id = id_

        self._inputs = []
        self._outputs = []

        self._ip = 0
        self._modes = iter([])
        self._halted = False

    def run(self, inputs=None):
        self._inputs = iter(inputs or [])

        while not self._halted:
            op, modes = self._get_operation()
            self._modes = iter(modes)

            dbgprint(f"IP: ip: {self._ip}, op={op}, mode={modes}", end="")

            if op == Op.ADD:
                self.add()
            elif op == Op.MUL:
                self.mul()
            elif op == Op.READ:
                self.read()
            elif op == Op.WRITE:
                self.write()
            elif op == Op.BNE:
                self.bne()
            elif op == Op.BEQ:
                self.beq()
            elif op == Op.LT:
                self.lt()
            elif op == Op.EQ:
                self.eq()
            elif op == Op.HALT:
                self.halt()
            else:
                dbgprint(", ERROR")
                dbgprint(self._intcodes)
                raise ValueError(f"Unsupported op: {op}")

    def _get_operation(self):
        op = self._intcodes[self._ip]
        opcode = op % 100
        modes = []

        op //= 100

        while op > 0:
            modes.append(op % 10)
            op //= 10

        return opcode, modes

    def _get_op_params(self, n):
        return self._intcodes[self._ip + 1 : self._ip + 1 + n]

    def add(self):
        p1, p2, out = self._get_op_params(3)
        dbgprint(f", p1={p1}, p2={p2}, out={out}")

        v1 = self._ld(p1, next(self._modes, 0))
        v2 = self._ld(p2, next(self._modes, 0))
        self._st(out, v1 + v2)

        self._ip += 4

    def mul(self):
        p1, p2, out = self._get_op_params(3)
        dbgprint(f", p1={p1}, p2={p2}, out={out}")

        v1 = self._ld(p1, next(self._modes, 0))
        v2 = self._ld(p2, next(self._modes, 0))
        self._st(out, v1 * v2)

        self._ip += 4

    def read(self):
        (out,) = self._get_op_params(1)
        dbgprint(f", out={out}")

        v = next(self._inputs, None)
        if v is None:
            raise WaitingOnInput()

        self._st(out, v)

        self._ip += 2

    def write(self):
        (p,) = self._get_op_params(1)
        dbgprint(f", p={p}")

        v = self._ld(p, next(self._modes, 0))
        self._outputs.append(v)

        self._ip += 2

    def bne(self):
        p1, p2 = self._get_op_params(2)
        dbgprint(f", p1={p1}, p2={p2}")

        v1 = self._ld(p1, next(self._modes, 0))
        v2 = self._ld(p2, next(self._modes, 0))

        if v1 != 0:
            self._ip = v2
        else:
            self._ip += 3

    def beq(self):
        p1, p2 = self._get_op_params(2)
        dbgprint(f", p1={p1}, p2={p2}")

        v1 = self._ld(p1, next(self._modes, 0))
        v2 = self._ld(p2, next(self._modes, 0))

        if v1 == 0:
            self._ip = v2
        else:
            self._ip += 3

    def lt(self):
        p1, p2, out = self._get_op_params(3)
        dbgprint(f", p1={p1}, p2={p2}, out={out}")

        v1 = self._ld(p1, next(self._modes, 0))
        v2 = self._ld(p2, next(self._modes, 0))

        if v1 < v2:
            self._st(out, 1)
        else:
            self._st(out, 0)

        self._ip += 4

    def eq(self):
        p1, p2, out = self._get_op_params(3)
        dbgprint(f", p1={p1}, p2={p2}, out={out}")

        v1 = self._ld(p1, next(self._modes, 0))
        v2 = self._ld(p2, next(self._modes, 0))

        if v1 == v2:
            self._st(out, 1)
        else:
            self._st(out, 0)

        self._ip += 4

    def halt(self):
        dbgprint(", exiting")

        self._halted = True

    def poke(self, idx):
        return self._intcodes[idx]

    def pop_outputs(self):
        outputs = self._outputs
        self._outputs = []
        return outputs

    def _ld(self, addr, mode=0):
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

    def __repr__(self):
        return f"{type(self).__name__}<{self._id}>"


class WaitingOnInput(Exception):
    pass
