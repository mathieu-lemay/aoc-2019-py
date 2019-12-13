#! /usr/bin/env python

import itertools

from aoc.intcode import IntCodeCPU, Interrupt
from aoc.utils import load_input


def get_thruster_output(program, phase_settings):
    outputs = []

    for ps in phase_settings:
        inputs = (ps, outputs[0] if outputs else 0)
        runner = IntCodeCPU(program, ps)
        runner.run(inputs)
        outputs = runner.pop_output()

    return outputs[0]


def get_thruster_output_with_feedback(program, phase_settings):
    cr = 0
    nb_runners = len(phase_settings)
    runners = [None] * nb_runners

    output = []

    def _get_runner(n):
        r = runners[n]
        if not r:
            r = IntCodeCPU(program, n)
            runners[n] = r

        return r

    while True:
        runner = _get_runner(cr % nb_runners)

        if cr < nb_runners:
            inputs = (phase_settings[cr], output[0] if output else 0)
        else:
            inputs = output

        try:
            runner.run(inputs)
        except Exception as e:
            print(e)
        else:
            if all(r.is_halted() for r in runners):
                return runner.pop_output()[0]

        output = runner.pop_output()

        cr += 1


def main():
    program = load_input("d07.txt")

    p1 = max(get_thruster_output(program, ps) for ps in itertools.permutations(range(5)))
    print(f"Part 1: {p1}")

    p2 = max(get_thruster_output_with_feedback(program, ps) for ps in itertools.permutations(range(5, 10)))
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    from time import time as ts

    _t = ts()
    main()
    _t = ts() - _t

    print(f"Took {_t:.3f}s")
