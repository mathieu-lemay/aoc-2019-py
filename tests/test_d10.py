from unittest import TestCase

from aoc.d10 import get_asteroids, get_best_asteroid, get_deg, obliterate


def parse_map(map_str):
    return [list(l) for l in map_str.split("\n")]


class D10Tests(TestCase):
    def test_get_deg(self):
        params = (
            (0, -1, 0),
            (1, -1, 45),
            (1, 0, 90),
            (1, 1, 135),
            (0, 1, 180),
            (-1, 1, 225),
            (-1, 0, 270),
            (-1, -1, 315),
        )

        for x, y, deg in params:
            with self.subTest(x=x, y=y, deg=deg):
                self.assertEqual(deg, get_deg(x, y))

    def test_p1_a(self):
        m = "......#.#.\n#..#.#....\n..#######.\n.#.#.###..\n.#..#.....\n..#....#.#\n#..#....#.\n.##.#..###\n##...#..#.\n.#....####"
        m = parse_map(m)
        asteroids = get_asteroids(m)
        a = get_best_asteroid(asteroids)
        self.assertEqual(5, a.x)
        self.assertEqual(8, a.y)
        self.assertEqual(33, a.nb_in_sight)

    def test_p1_b(self):
        m = "#.#...#.#.\n.###....#.\n.#....#...\n##.#.#.#.#\n....#.#.#.\n.##..###.#\n..#...##..\n..##....##\n......#...\n.####.###."
        m = parse_map(m)
        asteroids = get_asteroids(m)
        a = get_best_asteroid(asteroids)
        self.assertEqual(1, a.x)
        self.assertEqual(2, a.y)
        self.assertEqual(35, a.nb_in_sight)

    def test_p1_c(self):
        m = ".#..#..###\n####.###.#\n....###.#.\n..###.##.#\n##.##.#.#.\n....###..#\n..#.#..#.#\n#..#.#.###\n.##...##.#\n.....#.#.."
        m = parse_map(m)
        asteroids = get_asteroids(m)
        a = get_best_asteroid(asteroids)
        self.assertEqual(6, a.x)
        self.assertEqual(3, a.y)
        self.assertEqual(41, a.nb_in_sight)

    def test_p1_d(self):
        m = ".#..##.###...#######\n##.############..##.\n.#.######.########.#\n.###.#######.####.#.\n#####.##.#.##.###.##\n..#####..#.#########\n####################\n#.####....###.#.#.##\n##.#################\n#####.##.###..####..\n..######..##.#######\n####.##.####...##..#\n.#####..#.######.###\n##...#.##########...\n#.##########.#######\n.####.#.###.###.#.##\n....##.##.###..#####\n.#.#.###########.###\n#.#.#.#####.####.###\n###.##.####.##.#..##"
        m = parse_map(m)
        asteroids = get_asteroids(m)
        a = get_best_asteroid(asteroids)
        self.assertEqual(11, a.x)
        self.assertEqual(13, a.y)
        self.assertEqual(210, a.nb_in_sight)

    def test_p2(self):
        m = ".#....#####...#..\n##...##.#####..##\n##...#...#.#####.\n..#.....#...###..\n..#.#.....#....##"
        m = parse_map(m)
        asteroids = get_asteroids(m)
        a = get_best_asteroid(asteroids)
        self.assertEqual(8, a.x)
        self.assertEqual(3, a.y)

        params = (
            (1, (8, 1)),
            (9, (15, 1)),
            (18, (4, 4)),
            (27, (5, 1)),
        )

        for n, coords in params:
            tgt = obliterate(a, asteroids, n)
            self.assertEqual(coords, tgt.coords)
