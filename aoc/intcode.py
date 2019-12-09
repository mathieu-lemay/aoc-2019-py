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
    REL_OFFSET = 9
    HALT = 99


class IntCodeCPU:
    def __init__(self, program, id_=0):
        if isinstance(program, str):
            self._intcodes = [int(i) for i in program.split(",")]
        else:
            self._intcodes = program

        self._id = id_

        self._input = []
        self._output = []

        self._ip = 0
        self._rel_offset = 0
        self._ram_size = len(self._intcodes)
        self._modes = iter([])
        self._halted = False

        self._instr_map = {
            Op.ADD: self.add,
            Op.MUL: self.mul,
            Op.READ: self.read,
            Op.WRITE: self.write,
            Op.BNE: self.bne,
            Op.BEQ: self.beq,
            Op.LT: self.lt,
            Op.EQ: self.eq,
            Op.REL_OFFSET: self.rel_off,
            Op.HALT: self.halt,
        }

    def run(self, input_=None):
        self._input = iter(input_ or [])

        while not self._halted:
            instr, modes = self._get_instruction()
            self._modes = iter(modes)

            dbgprint(f"IP: ip: {self._ip}, instr={instr}, mode={modes}", end="")

            try:
                op = self._instr_map[instr]
            except KeyError:
                dbgprint(", ERROR")
                dbgprint(self._intcodes)
                raise ValueError(f"Unsupported instr: {instr}")

            op()

    def is_halted(self):
        return self._halted

    def _get_instruction(self):
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
        self._st(out, v1 + v2, next(self._modes, 0))

        self._ip += 4

    def mul(self):
        p1, p2, out = self._get_op_params(3)
        dbgprint(f", p1={p1}, p2={p2}, out={out}")

        v1 = self._ld(p1, next(self._modes, 0))
        v2 = self._ld(p2, next(self._modes, 0))
        self._st(out, v1 * v2, next(self._modes, 0))

        self._ip += 4

    def read(self):
        (out,) = self._get_op_params(1)
        dbgprint(f", out={out}")

        v = next(self._input, None)
        if v is None:
            raise WaitingOnInput()

        self._st(out, v, next(self._modes, 0))

        self._ip += 2

    def write(self):
        (p,) = self._get_op_params(1)
        dbgprint(f", p={p}")

        v = self._ld(p, next(self._modes, 0))
        self._output.append(v)

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
            self._st(out, 1, next(self._modes, 0))
        else:
            self._st(out, 0, next(self._modes, 0))

        self._ip += 4

    def eq(self):
        p1, p2, out = self._get_op_params(3)
        dbgprint(f", p1={p1}, p2={p2}, out={out}")

        v1 = self._ld(p1, next(self._modes, 0))
        v2 = self._ld(p2, next(self._modes, 0))

        if v1 == v2:
            self._st(out, 1, next(self._modes, 0))
        else:
            self._st(out, 0, next(self._modes, 0))

        self._ip += 4

    def rel_off(self):
        (p,) = self._get_op_params(1)
        dbgprint(f", p={p}")

        v = self._ld(p, next(self._modes, 0))

        self._rel_offset += v

        self._ip += 2

    def halt(self):
        dbgprint(", exiting")

        self._halted = True

    def poke(self, idx):
        return self._intcodes[idx]

    def pop_output(self):
        output = self._output
        self._output = []
        return output

    def _ld(self, addr, mode):
        dbgprint(f"LD: addr={addr}, mode={mode}")
        if mode == 0:
            return self._peek(addr)
        elif mode == 1:
            return addr
        elif mode == 2:
            return self._peek(addr + self._rel_offset)
        else:
            raise ValueError(f"Unsupported mode: {mode}")

    def _st(self, addr, v, mode):
        dbgprint(f"ST: addr={addr}, v={v}, mode={mode}")
        if mode == 0:
            return self._poke(addr, v)
        elif mode == 2:
            return self._poke(addr + self._rel_offset, v)
        else:
            raise ValueError(f"Unsupported mode: {mode}")

    def _peek(self, addr):
        if addr >= self._ram_size:
            self._extend_ram_to(addr)

        return self._intcodes[addr]

    def _poke(self, addr, v):
        if addr >= self._ram_size:
            self._extend_ram_to(addr)

        self._intcodes[addr] = v

    def _extend_ram_to(self, addr):
        ram_needed = addr + 1 - self._ram_size

        self._intcodes += [0] * ram_needed
        self._ram_size += ram_needed

    def __repr__(self):
        return f"{type(self).__name__}<{self._id}>"


class WaitingOnInput(Exception):
    pass
