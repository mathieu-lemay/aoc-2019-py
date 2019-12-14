#! /usr/bin/env python
import itertools
import math
import re
from typing import Dict

from aoc.utils import load_input_by_line


class Chemical:
    def __init__(self, name, qty):
        self.name = name
        self.qty = qty

    def __eq__(self, o):
        return self.name == o.name and self.qty == o.qty

    def __repr__(self):
        return f"Chemical(name={self.name}, qty={self.qty})"


class Reaction:
    def __init__(self, inputs: [Chemical], output: Chemical):
        self.inputs = inputs
        self.output = output
        self._input_chem_names = {c.name for c in inputs}

    @property
    def input_names(self):
        return self._input_chem_names

    def __eq__(self, o):
        return self.inputs == o.inputs and self.output == o.output

    def __repr__(self):
        return f"Reaction(inputs={self.inputs}, output={self.output})"


def parse_reactions(input_values: [str]) -> Dict[str, Reaction]:
    matcher = re.compile(r"([0-9]+) ([A-Z]+)")
    reactions = {}

    for iv in input_values:
        inputs = []
        raw_in, raw_out = iv.split(" => ")
        for in_ in [i.strip() for i in raw_in.split(",")]:
            m = matcher.match(in_)
            if not m:
                raise ValueError(f"Invalid input: {iv}")

            inputs.append(Chemical(m.group(2), int(m.group(1))))

        m = matcher.match(raw_out.strip())
        if not m:
            raise ValueError(f"Invalid input: {iv}")

        output = Chemical(m.group(2), int(m.group(1)))

        reactions[output.name] = Reaction(inputs, output)

    return reactions


def substitute(chemicals: [Chemical], reactions: Dict[str, Reaction], no_waste=False):
    chem = next(c for c in chemicals if not any(c.name in r.input_names for r in reactions.values()))

    chemicals = [c for c in chemicals if c != chem]
    r = reactions.pop(chem.name)
    ratio = chem.qty / r.output.qty if no_waste else math.ceil(chem.qty / r.output.qty)
    chemicals += [Chemical(c.name, c.qty * ratio) for c in r.inputs]

    return chemicals


def merge(chemicals: [Chemical]):
    chemicals.sort(key=lambda x: x.name)
    return [Chemical(k, sum(i.qty for i in values)) for k, values in itertools.groupby(chemicals, lambda x: x.name)]


def get_ore_needed(reactions: Dict[str, Reaction], no_waste=False):
    reaction = reactions.pop("FUEL")

    chemicals = reaction.inputs

    while reactions:
        chemicals = substitute(chemicals, reactions, no_waste)
        chemicals = merge(chemicals)

    if len(chemicals) != 1:
        raise ValueError(chemicals)

    chem = chemicals[0]
    if chem.name != "ORE":
        raise ValueError(chem)

    return chem.qty


def get_fuel_for_ore(reactions: Dict[str, Reaction], ore_amt):
    ore_per_fuel = get_ore_needed(reactions, no_waste=True)
    return math.floor(ore_amt / ore_per_fuel)


def main():
    input_values = load_input_by_line("d14.txt")
    reactions = parse_reactions(input_values)
    print(f"Part 1: {get_ore_needed(reactions.copy())}")
    print(f"Part 2: {get_fuel_for_ore(reactions.copy(), 1000_000_000_000)-1}")


if __name__ == "__main__":
    from time import time as ts

    _t = ts()
    main()
    _t = ts() - _t

    print(f"Runtime: {_t:.3f}s")
