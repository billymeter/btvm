#!/usr/bin/env python3
"""
the btvm assembler
"""

from common.common import *

opcode_lookup = {
    (opcode, address_mode): code for code, (opcode, address_mode) in opcodes.items()
}

syscall_lookup = {syscall: opcode for opcode, syscall in syscall_table.items()}


def assemble(nodes):
    program = "bt_x0008"
    for node in nodes:
        if isinstance(node, Node):
            opcode = opcode_lookup[(node.opcode, node.address_mode)]
            program += opcode.decode("utf-8")

            if isinstance(node.op1, int):
                program += "{:04x}".format(node.op1)
            elif node.op1 is None:
                program += "bt"
            else:
                program += node.op1

            if isinstance(node.op2, int):
                program += "{:04x}".format(node.op2)
            elif node.op2 is None:
                program += "btbt"
            elif (
                node.address_mode == AddressMode.REGISTER
                or node.address_mode == AddressMode.REGISTERDEREF
            ):
                program += node.op2 + "bt"
            else:
                program += node.op2

        else:
            program += node
    return program
