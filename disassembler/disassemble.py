#!/usr/bin/env python3
"""
the btvm disassembler
"""

from common.common import *


def register_to_str(register):
    if register == Register.R0:
        return "r0"
    if register == Register.R1:
        return "r1"
    if register == Register.R2:
        return "r2"
    if register == Register.R3:
        return "r3"
    if register == Register.R4:
        return "r4"
    if register == Register.R5:
        return "r5"
    if register == Register.R6:
        return "r6"
    if register == Register.R7:
        return "r7"
    if register == Register.RSP:
        return "rsp"
    if register == Register.RBP:
        return "rbp"
    if register == Register.RRES:
        return "rres"
    if register == Register.RERROR:
        return "rerror"
    return ""


def disassemble_add(mode, op1, op2):
    if mode == AddressMode.MEMORY:
        return f"add {op1} [{op2}]\n"
    return f"add {op1} {op2}\n"


def disassemble_and(mode, op1, op2):
    return ""


def disassemble_call(mode, op1, op2):
    return ""


def disassemble_compare(mode, op1, op2):
    return ""


def disassemble_divide(mode, op1, op2):
    return ""


def disassemble_input(mode, op1, op2):
    return ""


def disassemble_jump(mode, op1, op2):
    return ""


def disassemble_jumpeq(mode, op1, op2):
    return ""


def disassemble_jumpgreater(mode, op1, op2):
    return ""


def disassemble_jumpgreatereq(mode, op1, op2):
    return ""


def disassemble_jumpless(mode, op1, op2):
    return ""


def disassemble_jumplesseq(mode, op1, op2):
    return ""


def disassemble_jumpnoteq(mode, op1, op2):
    return ""


def disassemble_load(mode, op1, op2):
    return ""


def disassemble_loadbyte(mode, op1, op2):
    return ""


def disassemble_modulus(mode, op1, op2):
    return ""


def disassemble_multiply(mode, op1, op2):
    return ""


def disassemble_not(mode, op1, op2):
    return ""


def disassemble_or(mode, op1, op2):
    return ""


def disassemble_output(mode, op1, op2):
    return ""


def disassemble_pop(mode, op1, op2):
    return ""


def disassemble_popbyte(mode, op1, op2):
    return ""


def disassemble_push(mode, op1, op2):
    return ""


def disassemble_pushbyte(mode, op1, op2):
    return ""


def disassemble_store(mode, op1, op2):
    return ""


def disassemble_storebyte(mode, op1, op2):
    return ""


def disassemble_subtract(mode, op1, op2):
    return ""


def disassemble_xor(mode, op1, op2):
    return ""


def disassmble_instruction(instruction):
    if len(instruction) < 8:
        return ""
    opcode = instruction[:2]
    try:
        opcode, mode = opcodes[opcode]
    except KeyError:
        return "??\n"

    op1 = instruction[2:4]
    op1 = register_to_str(register_codes[op1])
    op2 = instruction[4:]

    if mode == AddressMode.LITERAL or mode == AddressMode.MEMORY:
        op2 = int(op2, 16)

    if Opcode.ADD == opcode:
        return disassemble_add(mode, op1, op2)
    if Opcode.AND == opcode:
        return disassemble_and(mode, op1, op2)
    if Opcode.CALL == opcode:
        return disassemble_call(mode, op1, op2)
    if Opcode.COMPARE == opcode:
        return disassemble_compare(mode, op1, op2)
    if Opcode.DIVIDE == opcode:
        return disassemble_divide(mode, op1, op2)
    if Opcode.HALT == opcode:
        return "halt\n"
    if Opcode.INPUT == opcode:
        return disassemble_input(mode, op1, op2)
    elif Opcode.JUMP == opcode:
        return disassemble_jump(mode, op1, op2)
    elif Opcode.JUMPEQ == opcode:
        return disassemble_jumpeq(mode, op1, op2)
    elif Opcode.JUMPGREATER == opcode:
        return disassemble_jumpgreater(mode, op1, op2)
    elif Opcode.JUMPGREATEREQ == opcode:
        return disassemble_jumpgreatereq(mode, op1, op2)
    elif Opcode.JUMPLESS == opcode:
        return disassemble_jumpless(mode, op1, op2)
    elif Opcode.JUMPLESSEQ == opcode:
        return disassemble_jumplesseq(mode, op1, op2)
    elif Opcode.JUMPNOTEQ == opcode:
        return disassemble_jumpnoteq(mode, op1, op2)
    elif Opcode.LOAD == opcode:
        return disassemble_load(mode, op1, op2)
    elif Opcode.LOADBYTE == opcode:
        return disassemble_loadbyte(mode, op1, op2)
    elif Opcode.MODULUS == opcode:
        return disassemble_modulus(mode, op1, op2)
    elif Opcode.MULTIPLY == opcode:
        return disassemble_multiply(mode, op1, op2)
    elif Opcode.NOP == opcode:
        return "nop\n"
    elif Opcode.NOT == opcode:
        return disassemble_not(mode, op1, op2)
    elif Opcode.OR == opcode:
        return disassemble_or(mode, op1, op2)
    elif Opcode.OUTPUT == opcode:
        return disassemble_output(mode, op1, op2)
    elif Opcode.POP == opcode:
        return disassemble_pop(mode, op1, op2)
    elif Opcode.POPBYTE == opcode:
        return disassemble_popbyte(mode, op1, op2)
    elif Opcode.PUSH == opcode:
        return disassemble_push(mode, op1, op2)
    elif Opcode.PUSHBYTE == opcode:
        return disassemble_pushbyte(mode, op1, op2)
    elif Opcode.RETURN == opcode:
        return "return\n"
    elif Opcode.STORE == opcode:
        return disassemble_store(mode, op1, op2)
    elif Opcode.STOREBYTE == opcode:
        return disassemble_storebyte(mode, op1, op2)
    elif Opcode.SUBTRACT == opcode:
        return disassemble_subtract(mode, op1, op2)
    elif Opcode.SYSCALL == opcode:
        return "syscall\n"
    elif Opcode.XOR == opcode:
        return disassemble_xor(mode, op1, op2)


def disassemble(program):
    source = ""
    # break up program into 8 byte blocks
    # TODO: figure out demarcation point between instructions and data. track references?
    instructions = [program[i : i + 8] for i in range(0, len(program), 8)][1:]
    print(instructions)
    for instruction in instructions:
        source += disassmble_instruction(bytes(instruction, "utf-8"))
    print(source)
