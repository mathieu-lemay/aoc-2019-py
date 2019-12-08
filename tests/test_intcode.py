from unittest import TestCase

from aoc.intcode import IntCodeCPU, WaitingOnInput


class IntCodeCPUTest(TestCase):
    def test_get_operation(self):
        params = (
            (1, (1, [])),
            (101102, (2, [1, 1, 0, 1])),
        )

        for op, expected in params:
            cpu = IntCodeCPU([op])
            self.assertEqual(expected, cpu._get_operation())

    def test_add(self):
        program = [1, 5, 6, 7, 99, 5, 8, 0]
        cpu = IntCodeCPU(program)
        cpu.run()

        self.assertEqual(13, cpu.poke(7))

    def test_mul(self):
        program = [2, 5, 6, 7, 99, 5, 8, 0]
        cpu = IntCodeCPU(program)
        cpu.run()

        self.assertEqual(40, cpu.poke(7))

    def test_read_with_input(self):
        program = [3, 3, 99, 0]
        cpu = IntCodeCPU(program)
        cpu.run((42,))

        self.assertEqual(42, cpu.poke(3))

    def test_read_no_input(self):
        program = [3, 3, 99, 0]
        cpu = IntCodeCPU(program)

        with self.assertRaises(WaitingOnInput):
            cpu.run()

        self.assertEqual(0, cpu._ip)

    def test_write(self):
        program = [4, 3, 99, 42]
        cpu = IntCodeCPU(program)
        cpu.run()

        self.assertEqual([42], cpu.pop_outputs())

    def test_bne_jump(self):
        program = [5, 0, 4, 42, 7, 0, 0, 99]
        cpu = IntCodeCPU(program)
        cpu.run()

        self.assertEqual(7, cpu._ip)

    def test_bne_no_jump(self):
        program = [5, 4, 3, 99, 0, 0, 0, 0]
        cpu = IntCodeCPU(program)
        cpu.run()
        self.assertEqual(3, cpu._ip)

    def test_beq_jump(self):
        program = [6, 5, 4, 42, 7, 0, 0, 99]
        cpu = IntCodeCPU(program)
        cpu.run()

        self.assertEqual(7, cpu._ip)

    def test_beq_no_jump(self):
        program = [6, 0, 3, 99, 0, 0, 0, 0]
        cpu = IntCodeCPU(program)
        cpu.run()
        self.assertEqual(3, cpu._ip)

    def test_lt_is_lower(self):
        program = [7, 5, 6, 7, 99, 5, 8, 42]
        cpu = IntCodeCPU(program)
        cpu.run()
        self.assertEqual(1, cpu.poke(7))

    def test_lt_is_not_lower(self):
        program = [7, 5, 6, 7, 99, 8, 5, 42]
        cpu = IntCodeCPU(program)
        cpu.run()
        self.assertEqual(0, cpu.poke(7))

    def test_eq_is_equal(self):
        program = [8, 5, 6, 7, 99, 5, 5, 42]
        cpu = IntCodeCPU(program)
        cpu.run()
        self.assertEqual(1, cpu.poke(7))

    def test_eq_is_not_equal(self):
        program = [8, 5, 6, 7, 99, 8, 5, 42]
        cpu = IntCodeCPU(program)
        cpu.run()
        self.assertEqual(0, cpu.poke(7))
