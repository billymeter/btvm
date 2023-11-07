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

        self.machine.memory[0x5757] = 0x00
        self.machine.memory[0x5758] = 0x57

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
        self.machine.memory[0x5758] = 0x57
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
        self.machine.memory[0x5758] = 0x57

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
        self.machine.memory[0x5758] = 0x57
        self.machine.registers[Register.R0] = 0xFFFF
        self.machine.registers[Register.R1] = 0x5757
        self.machine.run()
        self.assertEqual(
            self.machine.registers[Register.R0],
            0x57,
            "and r0 [r1] does not set value of r0 properly",
        )

    """CALL opcode tests"""

    def test_call_literal(self):
        # call label
        # halt
        # label:
        # add r0 1
        # halt
        program = b"bt_x0008clbt0018HTbtbtbtadr10001HTbtbtbt"
        self.machine = Machine(program)

        self.machine.run()
        self.assertEqual(
            self.machine.registers[Register.RSP],
            0xFFFD,
            "rsp does not equal 0xfffd (return address was not pushed to stack)",
        )
        self.assertEqual(
            self.machine.registers[Register.R1],
            1,
            "r1 does not equal 1",
        )

    def test_call_memory(self):
        # call [0x5000]
        # halt
        # label:
        # add r1 1
        # halt
        program = b"bt_x0008cLbt5000HTbtbtbtadr10001HTbtbtbt"
        self.machine = Machine(program)
        self.machine.memory[0x5000] = 0x00
        self.machine.memory[0x5001] = 0x18  # address of where label starts

        self.machine.run()
        self.assertEqual(
            self.machine.registers[Register.RSP],
            0xFFFD,
            "rsp does not equal 0xfffd (return address was not pushed to stack)",
        )
        self.assertEqual(
            self.machine.registers[Register.R1],
            1,
            "r1 does not equal 1",
        )

    def test_call_register(self):
        # push label
        # pop r0
        # call r0
        # halt
        # label:
        # add r1 1
        # halt
        program = b"bt_x0008pubt0028Por0btbtClbtr0btHTbtbtbtadr10001HTbtbtbt"
        self.machine = Machine(program)

        self.machine.run()
        self.assertEqual(
            self.machine.registers[Register.RSP],
            0xFFFD,
            "rsp does not equal 0xfffd (return address was not pushed to stack)",
        )
        self.assertEqual(
            self.machine.registers[Register.R1],
            1,
            "r1 does not equal 1",
        )

    def test_call_registerderef(self):
        # load r0 0x6165
        # call [r0]
        # halt
        # label:
        # add r1 1
        # halt
        program = b"bt_x0008ldr06164CLbtr0btHTbtbtbtadr10001HTbtbtbt"
        self.machine = Machine(program)
        self.machine.memory[0x6165] = 0x20

        self.machine.run()
        self.assertEqual(
            self.machine.registers[Register.RSP],
            0xFFFD,
            "rsp does not equal 0xfffd (return address was not pushed to stack)",
        )
        self.assertEqual(
            self.machine.registers[Register.R1],
            1,
            "r1 does not equal 1",
        )


if __name__ == "__main__":
    unittest.main()
