#!/usr/bin/env python3
"""
the btvm test suite
"""
from common.common import *
from vm.machine import Machine
import unittest


class TestVM(unittest.TestCase):
    """add opcode tests"""

    def test_add_literal(self):
        # add r0 0x5757
        # halt
        program = b"bt_x0008adr05757HTbtbtbt"
        self.machine = Machine(program)

        self.machine.run()
        self.assertEqual(
            self.machine.registers[Register.R0],
            0x5757,
            "add r0 0x5757 does not set value of r0 properly",
        )

    def test_add_memory(self):
        # add r0 [0x5757]
        # halt
        program = b"bt_x0008aDr05757HTbtbtbt"
        self.machine = Machine(program)
        self.machine.memory[0x5757] = 0x57

        self.machine.run()
        self.assertEqual(
            self.machine.registers[Register.R0],
            0x57,
            "add r0 [0x5757] does not set value of r0 properly",
        )

    def test_add_register(self):
        # add r0 0x5757
        # halt
        program = b"bt_x0008Adr0r1btHTbtbtbt"
        self.machine = Machine(program)
        self.machine.registers[Register.R0] = 0x79
        self.machine.registers[Register.R1] = 0x57

        self.machine.run()
        self.assertEqual(
            self.machine.registers[Register.R0],
            0xD0,
            "add r0 r1 does not set value of r0 properly",
        )

    def test_add_registerderef(self):
        # add r0 [r1]
        # halt
        program = b"bt_x0008ADr0r1btHTbtbtbt"
        self.machine = Machine(program)
        self.machine.memory[0x5757] = 0x57
        self.machine.registers[Register.R0] = 0x5700
        self.machine.registers[Register.R1] = 0x5757
        self.machine.run()
        self.assertEqual(
            self.machine.registers[Register.R0],
            0x5757,
            "add r0 [r1] does not set value of r0 properly",
        )

    """AND opcode tests"""

    def test_and_literal(self):
        # and r0 0x5757
        # halt
        program = b"bt_x0008anr05757HTbtbtbt"
        self.machine = Machine(program)
        self.machine.registers[Register.R0] = 0xFFFF

        self.machine.run()
        self.assertEqual(
            self.machine.registers[Register.R0],
            0x5757,
            "and r0 0x5757 does not set value of r0 properly",
        )

    def test_and_memory(self):
        # add r0 [0x5757]
        # halt
        program = b"bt_x0008aNr05757HTbtbtbt"
        self.machine = Machine(program)
        self.machine.registers[Register.R0] = 0xFFFF
        self.machine.memory[0x5757] = 0x57

        self.machine.run()
        self.assertEqual(
            self.machine.registers[Register.R0],
            0x57,
            "and r0 [0x5757] does not set value of r0 properly",
        )

    def test_and_register(self):
        # add r0 0x5757
        # halt
        program = b"bt_x0008Anr0r1btHTbtbtbt"
        self.machine = Machine(program)
        self.machine.registers[Register.R0] = 0x79
        self.machine.registers[Register.R1] = 0x57

        self.machine.run()
        self.assertEqual(
            self.machine.registers[Register.R0],
            0x51,
            "and r0 r1 does not set value of r0 properly",
        )

    def test_and_registerderef(self):
        # add r0 [r1]
        # halt
        program = b"bt_x0008ANr0r1btHTbtbtbt"
        self.machine = Machine(program)
        self.machine.memory[0x5757] = 0x57
        self.machine.registers[Register.R0] = 0xFFFF
        self.machine.registers[Register.R1] = 0x5757
        self.machine.run()
        self.assertEqual(
            self.machine.registers[Register.R0],
            0x57,
            "and r0 [r1] does not set value of r0 properly",
        )


if __name__ == "__main__":
    unittest.main()
