#! /usr/bin/env python

import itertools
import os
import unittest

_debug = os.getenv("DEBUG", "") != ""


def dbgprint(*args, **kwargs):
    if not _debug:
        return

    print(*args, **kwargs)


class IntCodeRunner:
    def __init__(self, id_, program):
        self._id = id_
        self._intcodes = [int(i) for i in program.split(",")]
        self._inputs = iter([])
        self._outputs = []
        self._ip = 0

    def run(self, inputs=None):
        self._inputs = iter(inputs or [])

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

                self._read(out)
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

        return self._outputs

    def pop_outputs(self):
        outputs = self._outputs
        self._outputs = []
        return outputs

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

    def _read(self, out):
        v = next(self._inputs, None)
        if v is None:
            self._ip -= 2
            raise self.WaitingOnInput()

        self._st(out, v)

    def _print(self, addr, mode):
        v = self._ld(addr, mode)
        self._outputs.append(v)

    class WaitingOnInput(Exception):
        pass

    def __repr__(self):
        return f"{type(self).__name__}<{self._id}>"


def get_thruster_output(program, phase_settings):
    outputs = []

    for ps in phase_settings:
        inputs = (ps, outputs[0] if outputs else 0)
        runner = IntCodeRunner(ps, program)
        outputs = runner.run(inputs)

    return outputs[0]


def get_thruster_output_with_feedback(program, phase_settings):
    cr = 0
    nb_runners = len(phase_settings)
    runners = [None] * nb_runners

    outputs = []

    def _get_runner(n):
        r = runners[n]
        if not r:
            r = IntCodeRunner(n, program)
            runners[n] = r

        return r

    while True:
        runner = _get_runner(cr % nb_runners)

        if cr < nb_runners:
            inputs = (phase_settings[cr], outputs[0] if outputs else 0)
        else:
            inputs = outputs

        try:
            runner.run(inputs)
        except IntCodeRunner.WaitingOnInput:
            pass
        except Exception as e:
            print(e)
        else:
            if (cr % nb_runners) == nb_runners - 1:
                return runner.pop_outputs()[0]

        outputs = runner.pop_outputs()

        cr += 1


def main():
    with open("input/d07.txt") as f:
        program = f.read()

    p1 = max(get_thruster_output(program, ps) for ps in itertools.permutations(range(5)))
    print(f"Part 1: {p1}")

    p2 = max(get_thruster_output_with_feedback(program, ps) for ps in itertools.permutations(range(5, 10)))
    print(f"Part 2: {p2}")


class Tests(unittest.TestCase):
    def test_p1(self):
        test_inputs = (
            ("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0", (4, 3, 2, 1, 0), 43210),
            ("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0", (0, 1, 2, 3, 4), 54321),
            (
                "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,"
                "1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0",
                (1, 0, 4, 3, 2),
                65210,
            ),
        )

        for program, phase_settings, expected in test_inputs:
            with self.subTest(program=program, phase_settings=phase_settings):
                self.assertEqual(expected, get_thruster_output(program, phase_settings))

    def test_p2(self):
        test_inputs = (
            (
                "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5",
                (9, 8, 7, 6, 5),
                139629729,
            ),
            (
                "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,"
                "54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10",
                (9, 7, 8, 5, 6),
                18216,
            ),
        )

        for program, phase_settings, expected in test_inputs:
            with self.subTest(program=program, phase_settings=phase_settings):
                self.assertEqual(expected, get_thruster_output_with_feedback(program, phase_settings))


def tests():
    suite = unittest.makeSuite(Tests)
    unittest.TextTestRunner().run(suite)
    print("\n----------------------------------------------------------------------\n")


if __name__ == "__main__":
    from time import time as ts

    tests()

    _t = ts()
    main()
    _t = ts() - _t

    print(f"Took {_t:.3f}s")
