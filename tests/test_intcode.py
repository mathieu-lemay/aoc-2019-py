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

        self.assertEqual([42], cpu.pop_output())

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

    def test_unsupported_intcode(self):
        program = [42]
        cpu = IntCodeCPU(program)
        with self.assertRaises(ValueError) as exc_ctx:
            cpu.run()

        self.assertEqual("Unsupported op: 42", str(exc_ctx.exception))

    def test_ld_mode_0(self):
        program = [0, 99]
        cpu = IntCodeCPU(program)
        self.assertEqual(99, cpu._ld(1, 0))

    def test_ld_mode_1(self):
        program = []
        cpu = IntCodeCPU(program)
        self.assertEqual(99, cpu._ld(99, 1))

    def test_ld_invalid_mode(self):
        program = []
        cpu = IntCodeCPU(program)
        with self.assertRaises(ValueError) as exc_ctx:
            cpu._ld(0, 42)

        self.assertEqual("Unsupported mode: 42", str(exc_ctx.exception))


class IntCodeProgramsTest(TestCase):
    def test_relative_mode_addressing(self):
        program = [int(i) for i in "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99".split(",")]
        cpu = IntCodeCPU(program[:])
        cpu.run()

        self.assertEqual(program, cpu.pop_output())

    def test_big_numbers(self):
        program = "1102,34915192,34915192,7,4,7,99,0"
        cpu = IntCodeCPU(program)
        cpu.run()

        self.assertEqual([1219070632396864], cpu.pop_output())

    def test_output_middle_number(self):
        program = "104,1125899906842624,99"
        cpu = IntCodeCPU(program[:])
        cpu.run()

        self.assertEqual([1125899906842624], cpu.pop_output())
