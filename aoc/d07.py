#! /usr/bin/env python

import itertools

from aoc.intcode import IntCodeRunner
from aoc.utils import load_input


def get_thruster_output(program, phase_settings):
    outputs = []

    for ps in phase_settings:
        inputs = (ps, outputs[0] if outputs else 0)
        runner = IntCodeRunner(program, ps)
        runner.run(inputs)
        outputs = runner.pop_outputs()

    return outputs[0]


def get_thruster_output_with_feedback(program, phase_settings):
    cr = 0
    nb_runners = len(phase_settings)
    runners = [None] * nb_runners

    outputs = []

    def _get_runner(n):
        r = runners[n]
        if not r:
            r = IntCodeRunner(program, n)
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
