#! /usr/bin/env python
import sys
from enum import IntEnum
from time import time as ts

from aoc.intcode import IntCodeCPU, InterruptCode
from aoc.utils import load_input


def log(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class Tile(IntEnum):
    UNKNOWN = 0
    EMPTY = 1
    WALL = 2
    OXYGEN = 3
    ROBOT = 4


class Direction(IntEnum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def translate(self, direction: Direction) -> "Point":
        delta = {Direction.UP: (0, -1), Direction.DOWN: (0, 1), Direction.LEFT: (-1, 0), Direction.RIGHT: (1, 0)}[
            direction
        ]

        return Point(self.x + delta[0], self.y + delta[1])

    @property
    def tuple(self):
        return self.x, self.y

    def __eq__(self, o):
        return self.x == o.x and self.y == o.y


class Robot:
    def __init__(self, x, y, direction):
        self.pos = Point(x, y)
        self.direction = direction

    def next_pos(self) -> Point:
        return self.pos.translate(self.direction)

    def set_pos(self, pos: Point):
        self.pos = pos

    def turn_right(self):
        self.direction = {
            Direction.UP: Direction.RIGHT,
            Direction.DOWN: Direction.LEFT,
            Direction.LEFT: Direction.UP,
            Direction.RIGHT: Direction.DOWN,
        }[self.direction]

    def turn_left(self):
        self.direction = {
            Direction.UP: Direction.LEFT,
            Direction.DOWN: Direction.RIGHT,
            Direction.LEFT: Direction.DOWN,
            Direction.RIGHT: Direction.UP,
        }[self.direction]


class Map:
    _char_map = {
        Tile.UNKNOWN: " ",
        Tile.EMPTY: " ",
        Tile.WALL: "\033[31m█\033[0m",
        Tile.OXYGEN: "\033[32m▣\033[0m",
        Tile.ROBOT: "\033[33m◉\033[0m",
    }

    def __init__(self, robot):
        self.robot = robot
        self.orig = Point(0, 0)
        self.oxy_pos = None
        self.tiles = {self.orig.tuple: Tile.EMPTY}
        self.h = 1
        self.w = 1

    def set_tile(self, x, y, tile: Tile):
        self.tiles[(x, y)] = tile

    def get_tile(self, x, y):
        return self.tiles.get((x, y), Tile.UNKNOWN)

    def get_walkable_tile_positions(self):
        return [k for k, v in self.tiles.items() if v != Tile.WALL]

    def render(self):
        print("\033[2J\033[0;0H")
        min_x = min(p[0] for p in self.tiles.keys())
        max_x = max(p[0] for p in self.tiles.keys())
        min_y = min(p[1] for p in self.tiles.keys())
        max_y = max(p[1] for p in self.tiles.keys())

        for y in range(min_y, max_y + 1):
            line = [self._char_map[self.get_tile(x, y)] for x in range(min_x, max_x + 1)]
            if self.robot.pos.y == y:
                line[self.robot.pos.x - min_x] = self._char_map[Tile.ROBOT]

            print("".join(line))


def generate_floor(program):
    robot = Robot(0, 0, Direction.UP)
    floor = Map(robot)

    cpu = IntCodeCPU(program)

    interrupt = cpu.run()
    if interrupt != InterruptCode.WAITING_ON_INPUT:
        raise ValueError(f"Unexpected program state: Interrupt = {interrupt}")

    while True:
        res = cpu.run((robot.direction,))
        out = cpu.pop_output()
        if len(out) > 1:
            raise ValueError(f"Output too long: {out}")

        out = out[0]
        new_pos = robot.next_pos()
        if out == 0:
            floor.set_tile(new_pos.x, new_pos.y, Tile.WALL)
            robot.turn_left()
        elif out == 1:
            floor.set_tile(new_pos.x, new_pos.y, Tile.EMPTY)
            robot.set_pos(new_pos)
            robot.turn_right()
        elif out == 2:
            floor.set_tile(new_pos.x, new_pos.y, Tile.OXYGEN)
            floor.oxy_pos = Point(new_pos.x, new_pos.y)
            robot.set_pos(new_pos)
            robot.turn_right()
        else:
            raise ValueError(f"Invalid output: {out}")

        if res is None or robot.pos == floor.orig:
            break

    return floor


def get_neighbors(p, points):
    return [x for x in points if (abs(p[0] - x[0]) + abs(p[1] - x[1])) == 1]


def get_distances_from(point, floor):
    remaining_tiles = floor.get_walkable_tile_positions()
    t = point.tuple
    distances = {t: 0}

    remaining_tiles.remove(t)
    todo = get_neighbors(t, remaining_tiles)
    for x in todo:
        remaining_tiles.remove(x)

    while len(todo) > 0:
        tile = todo.pop(0)
        dist = min(v for k, v in distances.items() if (abs(tile[0] - k[0]) + abs(tile[1] - k[1])) == 1) + 1
        distances[tile] = dist

        n = get_neighbors(tile, remaining_tiles)
        for x in n:
            remaining_tiles.remove(x)
            todo.append(x)

    return distances


def find_shortest_path(floor):
    distances = get_distances_from(Point(0, 0), floor)

    return distances[floor.oxy_pos.tuple]


def find_max_distance_from_oxy(floor):
    distances = get_distances_from(floor.oxy_pos, floor)

    return max(v for v in distances.values())


def main():
    program = load_input("d15.txt")
    floor = generate_floor(program)
    print(f"Part 1: {find_shortest_path(floor)}")
    print(f"Part 2: {find_max_distance_from_oxy(floor)}")


if __name__ == "__main__":

    _t = ts()
    main()
    _t = ts() - _t

    print(f"Runtime: {_t:.3f}s")
