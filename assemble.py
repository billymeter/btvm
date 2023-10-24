#!/usr/bin/env python3
"""
assembler for the btvm.
"""

# from ..vm.instruction import Instruction
from vm.util import opcodes, register_codes, AddressMode, Register, Opcode
import sys


class Program:
    def __init__(self):
        self.variables = dict()
        self.labels = dict()
        self.byte_pos = 0
        self.output = b""


def parse_line(line, program):
    line = line.split(" ")
    op = line[0].lower()
    if "add" == op:
        opcode = Opcode.ADD
    elif "and" == op:
        opcode = Opcode.AND
    elif "call" == op:
        opcode = Opcode.CALL
    elif "compare" == op:
        opcode = Opcode.COMPARE
    elif "divide" == op:
        opcode = Opcode.DIVIDE
    elif "halt" == op:
        opcode = Opcode.HALT
    elif "input" == op:
        opcode = Opcode.INPUT
    elif "jump" == op:
        opcode = Opcode.JUMP
    elif "jumpeq" == op:
        opcode = Opcode.JUMPEQ
    elif "jumpgreater" == op:
        opcode = Opcode.JUMPGREATER
    elif "jumpgreatereq" == op:
        opcode = Opcode.JUMPGREATEREQ
    elif "jumpless" == op:
        opcode = Opcode.JUMPLESS
    elif "jumplesseq" == op:
        opcode = Opcode.JUMPLESSEQ
    elif "jumpnoteq" == op:
        opcode = Opcode.JUMPNOTEQ
    elif "load" == op:
        opcode = Opcode.LOAD
    elif "loadbyte" == op:
        opcode = Opcode.LOADBYTE
    elif "modulus" == op:
        opcode = Opcode.MODULUS
    elif "multiply" == op:
        opcode = Opcode.MULTIPLY
    elif "nop" == op:
        opcode = Opcode.NOP
    elif "not" == op:
        opcode = Opcode.NOT
    elif "or" == op:
        opcode = Opcode.OR
    elif "output" == op:
        opcode = Opcode.OUTPUT
    elif "pop" == op:
        opcode = Opcode.POP
    elif "popbyte" == op:
        opcode = Opcode.POPBYTE
    elif "push" == op:
        opcode = Opcode.PUSH
    elif "pushbyte" == op:
        opcode = Opcode.PUSHBYTE
    elif "return" == op:
        opcode = Opcode.RETURN
    elif "store" == op:
        opcode = Opcode.STORE
    elif "storebyte" == op:
        opcode = Opcode.STOREBYTE
    elif "subtract" == op:
        opcode = Opcode.SUBTRACT
    elif "syscall" == op:
        opcode = Opcode.SYSCALL
    elif "xor" == op:
        opcode = Opcode.XOR
    else:
        opcode = Opcode.NONE

    return opcode


def parse_program(program):
    prog = Program()
    # parse line by line
    for line in program.split("\n"):
        # skip blank lines
        if not line:
            continue
        # strip off comments and whitespace
        line = parse_line(line.strip().split(";")[0].strip(), prog)
        print(line)


def main():
    if len(sys.argv) > 1:
        source_file = sys.argv[1]
        with open(source_file) as f:
            program = f.read()
            parse_program(program)
    else:
        help()


def help():
    print(f"usage: {sys.argv[0]} <source code file>")


if __name__ == "__main__":
    main()
