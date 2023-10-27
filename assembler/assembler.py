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
            # print(node)
            opcode = opcode_lookup[(node.opcode, node.address_mode)]
            program += opcode.decode("utf-8")
            # print(opcode.decode("utf-8"), end="")

            if isinstance(node.op1, int):
                program += "{:04x}".format(node.op1)
                # print("{:04x}".format(node.op1), end="")
            elif node.op1 is None:
                program += "bt"
                # print("bt", end="")
            else:
                program += node.op1
                # print(node.op1, end="")

            if isinstance(node.op2, int):
                program += "{:04x}".format(node.op2)
                # print("{:04x}".format(node.op2), end="")
            elif node.op2 is None:
                program += "btbt"
                # print("btbt", end="")
            else:
                program += node.op2
                print(node.op2, end="")

            # print()
        else:
            program += node
            # print(node, end="")
    return program
