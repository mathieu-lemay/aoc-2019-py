#! /usr/bin/env python
from enum import IntEnum

from aoc.intcode import IntCodeCPU, WaitingOnInput
from aoc.utils import load_input


class Color(IntEnum):
    BLACK = 0
    WHITE = 1


class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class TurnDirection(IntEnum):
    LEFT = 0
    RIGHT = 1


class Panel:
    def __init__(self, x, y, color=Color.BLACK, painted=False):
        self.x = x
        self.y = y
        self.color = color
        self.painted = painted

    def paint(self, color: Color):
        self.color = color
        self.painted = True


class Robot:
    def __init__(self, x, y, direction=Direction.UP):
        self.x = x
        self.y = y
        self.direction = direction

    def turn(self, td: TurnDirection):
        if td == TurnDirection.LEFT:
            self.direction = {
                Direction.UP: Direction.LEFT,
                Direction.DOWN: Direction.RIGHT,
                Direction.LEFT: Direction.DOWN,
                Direction.RIGHT: Direction.UP,
            }[self.direction]
        elif td == TurnDirection.RIGHT:
            self.direction = {
                Direction.UP: Direction.RIGHT,
                Direction.DOWN: Direction.LEFT,
                Direction.LEFT: Direction.UP,
                Direction.RIGHT: Direction.DOWN,
            }[self.direction]
        else:
            raise ValueError("Invalid Direction")

    def move_forward(self):
        move = {Direction.UP: (0, 1), Direction.DOWN: (0, -1), Direction.LEFT: (-1, 0), Direction.RIGHT: (1, 0),}[
            self.direction
        ]

        self.x += move[0]
        self.y += move[1]

    @property
    def position(self):
        return self.x, self.y


def run_robot(program, initial_coords, initial_color):
    panels = {initial_coords: Panel(*initial_coords, initial_color)}
    robot = Robot(*initial_coords)

    cpu = IntCodeCPU(program)

    while True:
        p = panels.get(robot.position)
        if not p:
            p = Panel(*robot.position)
            panels[robot.position] = p

        try:
            cpu.run((p.color.value,))
        except WaitingOnInput:
            c, td = cpu.pop_output()
            p.paint(Color(c))
            robot.turn(TurnDirection(td))
            robot.move_forward()
        else:
            break

    return panels


def render_panels(panels):
    panels = panels.values()

    min_x = min(p.x for p in panels)
    min_y = min(p.y for p in panels)

    for p in panels:
        p.x -= min_x
        p.y -= min_y

    w = max(p.x for p in panels) + 1
    h = max(p.y for p in panels) + 1

    render = []
    for i in range(h):
        render.append([" "] * w)

    for p in panels:
        if p.color == Color.WHITE:
            render[p.y][p.x] = "#"

    for row in reversed(render):
        print("".join(row))


def main():
    program = load_input("d11.txt")

    panels = run_robot(program, (0, 0), Color.BLACK)

    print(f"Part 1: {len([p for p in panels.values() if p.painted])}")

    panels = run_robot(program, (0, 0), Color.WHITE)

    print("Part 2:")
    render_panels(panels)


if __name__ == "__main__":
    from time import time as ts

    _t = ts()
    main()
    _t = ts() - _t

    print(f"Runtime: {_t:.3f}s")
