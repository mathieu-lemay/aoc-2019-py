#! /usr/bin/env python
import sys
from enum import IntEnum

from aoc.intcode import IntCodeCPU, InterruptCode
from aoc.utils import load_input, split_list


def get_blocks_after_first_run(program):
    cpu = IntCodeCPU(program)
    cpu.run()
    output = cpu.pop_output()

    c = 0
    for i in range(2, len(output), 3):
        if output[i] == 2:
            c += 1

    return c


class Tile(IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


class Pixel:
    def __init__(self, values):
        self.x = values[0]
        self.y = values[1]
        self.v = Tile(values[2])


class GameState:
    _char_map = {
        Tile.EMPTY: " ",
        Tile.WALL: "X",
        Tile.BLOCK: "#",
        Tile.PADDLE: "_",
        Tile.BALL: "O",
    }

    def __init__(self, w, h):
        self.w = w
        self.h = h

        self._tiles = [0] * (w * h)

        self._frame = 0
        self._score = 0
        self._blocks = 0
        self._paddle_pos = (0, 0)
        self._ball_pos = (0, 0)

    @property
    def score(self):
        return self._score

    @property
    def paddle_x(self):
        return self._paddle_pos[0]

    @property
    def ball_x(self):
        return self._ball_pos[0]

    @classmethod
    def init(cls, values) -> "GameState":
        pixels = [Pixel(t) for t in cls._get_tuples(values)]

        w = max(p.x for p in pixels) + 1
        h = max(p.y for p in pixels) + 1

        gs = cls(w, h)
        gs.set_tiles(pixels)

        return gs

    def update(self, values):
        self._frame += 1
        pixels = []

        for tup in split_list(values, 3):
            if tup[0] == -1:
                self._score = tup[2]
            else:
                pixels.append(Pixel(tup))

        self.set_tiles(pixels)

    @staticmethod
    def _get_tuples(values):
        for tup in split_list(values, 3):
            yield tuple(int(v) for v in tup)

    def set_tiles(self, pixels: [Pixel]):
        for p in pixels:
            self.set(p.x, p.y, p.v)

    def get(self, x, y) -> Tile:
        return self._tiles[y * self.w + x]

    def set(self, x, y, v):
        self._update_counters(x, y, v)
        self._tiles[y * self.w + x] = v

    def _update_counters(self, x, y, v):
        cv = self.get(x, y)
        if cv == Tile.EMPTY and v == Tile.BLOCK:
            self._blocks += 1
        elif cv == Tile.BLOCK and v == Tile.EMPTY:
            self._blocks -= 1
        elif v == Tile.PADDLE:
            self._paddle_pos = (x, y)
        elif v == Tile.BALL:
            self._ball_pos = (x, y)

    def render(self):
        print("\033[0;0H")
        print(f"Frame: {self._frame}, Score: {self._score}")
        for y in range(self.h):
            line = "".join(self._char_map[self.get(x, y)] for x in range(self.w))
            print(line)


def play(program, coins=2, render=False):
    if render:
        print("\033[2J")

    cpu = IntCodeCPU(program)
    cpu.poke(0, coins)

    interrupt = cpu.run()
    if interrupt != InterruptCode.WAITING_ON_INPUT:
        raise ValueError(f"Unexpected program state: Interrupt = {interrupt}")

    gs = GameState.init(cpu.pop_output())

    while True:
        delta = gs.ball_x - gs.paddle_x
        if delta > 0:
            in_ = (1,)
        elif delta < 0:
            in_ = (-1,)
        else:
            in_ = (0,)

        res = cpu.run(in_)
        gs.update(cpu.pop_output())

        if render:
            gs.render()
            sleep(0.015)

        if res is None:
            break

    return gs.score


def main():
    program = load_input("d13.txt")

    print(f"Part 1: {get_blocks_after_first_run(program)}")

    render = len(sys.argv) > 1 and sys.argv[1] == "-r"
    print(f"Part 2: {play(program, render=render)}")


if __name__ == "__main__":
    from time import time as ts, sleep

    _t = ts()
    main()
    _t = ts() - _t

    print(f"Runtime: {_t:.3f}s")
