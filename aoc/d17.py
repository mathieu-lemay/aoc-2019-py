#! /usr/bin/env python
import itertools
from enum import Enum
from time import time as ts

from aoc.intcode import IntCodeCPU
from aoc.utils import load_input


class Direction(Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


def find_block(data, block, offset):
    if not block:
        return []

    block_positions = []
    i = offset
    blen = len(block)
    while i < len(data):
        b = data[i : i + blen]
        if b == block:
            block_positions.append(i)
            i += blen
        else:
            i += 1

    return block_positions


def get_next_block(data, offset):
    block_len = 1
    block = data[offset : offset + block_len]
    block_positions = find_block(data, block, offset + block_len)

    while block_positions:
        block_len += 1
        block = data[offset : offset + block_len]
        if len(",".join(block)) > 20:
            break
        block_positions = find_block(data, block, offset + block_len)

    if block_len == 0:
        return [], []

    block_len -= 1
    block = data[offset : offset + block_len]
    block_positions = find_block(data, block, offset + block_len)

    return block, block_positions


def compress(data):
    offset = 0
    id_ = ord("A")

    compressed_blocks = []

    b, positions = get_next_block(data, offset)
    while positions:
        compressed_blocks.append((chr(id_), b))
        blen = len(b)
        id_ += 1
        for p in sorted(positions + [0], reverse=True):
            data = data[:p] + data[p + blen :]

        offset = 0
        b, positions = get_next_block(data, offset)

    return compressed_blocks


class Grid:
    def __init__(self, grid, pos, dir_):
        self.grid = grid
        self.w = len(grid[0])
        self.h = len(grid)

        self.robot_pos = pos
        self.robot_direction = dir_

    @classmethod
    def build(cls, program):
        cpu = IntCodeCPU(program)
        res = cpu.run()
        if res is not None:
            raise ValueError(f"CPU raised an interrupt: {res}")

        grid = "".join([chr(i) for i in cpu.pop_output()])

        grid = [list(r) for r in grid.split("\n") if r]

        direction_chars = {d.value for d in Direction}

        for x, y in itertools.product(range(len(grid[0])), range(len(grid))):
            if grid[y][x] in direction_chars:
                pos = (x, y)
                dir_ = Direction(grid[y][x])
                grid[y][x] = "#"
                break
        else:
            raise ValueError("Vacuum not found")

        return cls(grid, pos, dir_)

    def get_tile(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.grid[y][x]

        return None

    def get_junctions(self):
        jcts = []
        for x in range(self.w):
            for y in range(self.h):
                if (
                    self.get_tile(x, y) == "#"
                    and self.get_tile(x - 1, y) == "#"
                    and self.get_tile(x + 1, y) == "#"
                    and self.get_tile(x, y - 1) == "#"
                    and self.get_tile(x, y + 1) == "#"
                ):
                    jcts.append((x, y))

        return jcts

    def render(self):
        rows = []
        for y, row in enumerate(self.grid):
            if y == self.robot_pos[1]:
                r = row[:]
                r[self.robot_pos[0]] = "\033[31m" + self.robot_direction.value + "\033[0m"
            else:
                r = row

            rows.append("".join(r))

        print("\033[2J\033[0;0H")
        print("\n".join(rows))
        from time import sleep

        sleep(0.05)

    def get_dust_routine(self):
        movements, patterns = self.get_movements()

        return movements, patterns

    def get_movements(self):
        movements = []

        turn_direction = self.try_turn()
        while turn_direction is not None:
            nb_moves = self.move_robot_straight()
            movements.append(f"{turn_direction.name[0]}{nb_moves}")
            turn_direction = self.try_turn()

        patterns = [
            ("A", "R8,L10,R8"),
            ("B", "R12,R8,L8,L12"),
            ("C", "L12,L10,L8"),
        ]

        movements = ",".join(movements)

        for c in patterns:
            movements = movements.replace(c[1], c[0])

        return movements, patterns

    def try_turn(self):
        orig_direction = self.robot_direction

        self.turn_robot_left()
        if self.robot_can_move():
            return Direction.LEFT

        self.robot_direction = orig_direction
        self.turn_robot_right()
        if self.robot_can_move():
            return Direction.RIGHT

        self.robot_direction = orig_direction
        return None

    def move_robot_straight(self):
        n = 0
        while self.robot_can_move():
            self.step_robot()
            n += 1

        return n

    def turn_robot_left(self):
        self.robot_direction = {
            Direction.UP: Direction.LEFT,
            Direction.DOWN: Direction.RIGHT,
            Direction.LEFT: Direction.DOWN,
            Direction.RIGHT: Direction.UP,
        }[self.robot_direction]

    def turn_robot_right(self):
        self.robot_direction = {
            Direction.UP: Direction.RIGHT,
            Direction.DOWN: Direction.LEFT,
            Direction.LEFT: Direction.UP,
            Direction.RIGHT: Direction.DOWN,
        }[self.robot_direction]

    def robot_can_move(self):
        return self.get_next_robot_tile() == "#"

    def get_next_robot_tile(self):
        delta = {Direction.UP: (0, -1), Direction.DOWN: (0, 1), Direction.LEFT: (-1, 0), Direction.RIGHT: (1, 0),}[
            self.robot_direction
        ]

        return self.get_tile(self.robot_pos[0] + delta[0], self.robot_pos[1] + delta[1])

    def step_robot(self):
        delta = {Direction.UP: (0, -1), Direction.DOWN: (0, 1), Direction.LEFT: (-1, 0), Direction.RIGHT: (1, 0),}[
            self.robot_direction
        ]

        self.robot_pos = (self.robot_pos[0] + delta[0], self.robot_pos[1] + delta[1])


def main():
    program = load_input("d17.txt")
    grid = Grid.build(program)

    junctions = grid.get_junctions()
    p1 = sum(j[0] * j[1] for j in junctions)
    print(f"Part 1: {p1}")

    routine, functions = grid.get_dust_routine()

    def encode(data):
        x = [ord(c) for c in list(data)] + [10]
        if len(x) > 20:
            raise ValueError(data)

        return x

    def encode_fn(data):
        fn = []
        elements = data.split(",")
        for e in elements:
            fn.append(e[0])
            fn.append(str(e[1:]))

        return encode(",".join(fn))

    cpu = IntCodeCPU(program)
    cpu.poke(0, 2)
    cpu.run(encode(routine))
    for f in functions:
        cpu.run(encode_fn(f[1]))

    cpu.run(encode("n"))

    print(f"Part 2: {cpu.pop_output()[-1]}")

    # grid.render()


if __name__ == "__main__":
    _t = ts()
    main()
    _t = ts() - _t

    print(f"Runtime: {_t:.3f}s")
