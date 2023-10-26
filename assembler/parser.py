#!/usr/bin/env python3
"""
btvm assembler parser
"""

from common.common import *
import sys


opcode_lookup = {
    (opcode, address_mode): code for code, (opcode, address_mode) in opcodes.items()
}

syscall_lookup = {syscall: opcode for opcode, syscall in syscall_table.items()}

symbol_table = {}


def get_address_mode(operand1, operand2):
    if operand1.type == Type.REGISTER:
        return AddressMode.REGISTER
    if operand1.type == Type.LITERAL:
        operand1.value


def add_token(token, iter):
    first = next(iter)
    if first.type == Type.REGISTER:
        opcode = b"Ad"
    second = next(iter)
    print(f"{first} {second}")


def and_token(token, iter):
    pass


def call_token(token, iter):
    pass


def compare_token(token, iter):
    pass


def divide_token(token, iter):
    pass


def halt_token(token, iter):
    pass


def input_token(token, iter):
    pass


def jump_token(token, iter):
    pass


def jumpeq_token(token, iter):
    pass


def jumpgreater_token(token, iter):
    pass


def jumpgreatereq_token(token, iter):
    pass


def jumpless_token(token, iter):
    pass


def jumplesseq_token(token, iter):
    pass


def jumpnoteq_token(token, iter):
    pass


def load_token(token, iter):
    op1 = next(iter)
    op2 = next(iter)
    print(f"load {op1.value} {op2.value}")


def loadbyte_token(token, iter):
    pass


def modulus_token(token, iter):
    pass


def multiply_token(token, iter):
    pass


def nop_token(token, iter):
    pass


def not_token(token, iter):
    pass


def or_token(token, iter):
    pass


def output_token(token, iter):
    pass


def pop_token(token, iter):
    pass


def popbyte_token(token, iter):
    pass


def push_token(token, iter):
    pass


def pushbyte_token(token, iter):
    pass


def return_token(token, iter):
    pass


def store_token(token, iter):
    pass


def storebyte_token(token, iter):
    pass


def subtract_token(token, iter):
    pass


def syscall_token(token, iter):
    pass


def xor_token(token, iter):
    pass


def label_token(token, iter):
    pass


def literal_token(token, iter):
    pass


def register_token(token, iter):
    pass


def variable_token(token, iter):
    literal_token = next(iter)
    symbol_table[token.value] = literal_token.value


def parse(tokens):
    toks = iter(tokens)
    while True:
        token = next(toks, "end")
        if token == "end":
            break
        if token.type == Type.ADD:
            add_token(token, toks)
        if token.type == Type.AND:
            and_token(token, toks)
        if token.type == Type.CALL:
            call_token(token, toks)
        if token.type == Type.COMPARE:
            compare_token(token, toks)
        if token.type == Type.DIVIDE:
            divide_token(token, toks)
        if token.type == Type.HALT:
            halt_token(token, toks)
        if token.type == Type.INPUT:
            input_token(token, toks)
        if token.type == Type.JUMP:
            jump_token(token, toks)
        if token.type == Type.JUMPEQ:
            jumpeq_token(token, toks)
        if token.type == Type.JUMPGREATER:
            jumpgreater_token(token, toks)
        if token.type == Type.JUMPLESS:
            jumpless_token(token, toks)
        if token.type == Type.JUMPLESSEQ:
            jumplesseq_token(token, toks)
        if token.type == Type.JUMPNOTEQ:
            jumpnoteq_token(token, toks)
        if token.type == Type.LOAD:
            load_token(token, toks)
        if token.type == Type.LOADBYTE:
            loadbyte_token(token, toks)
        if token.type == Type.MODULUS:
            modulus_token(token, toks)
        if token.type == Type.MULTIPLY:
            multiply_token(token, toks)
        if token.type == Type.NOP:
            nop_token(token, toks)
        if token.type == Type.NOT:
            not_token(token, toks)
        if token.type == Type.OR:
            or_token(token, toks)
        if token.type == Type.OUTPUT:
            output_token(token, toks)
        if token.type == Type.POP:
            pop_token(token, toks)
        if token.type == Type.POPBYTE:
            popbyte_token(token, toks)
        if token.type == Type.PUSH:
            push_token(token, toks)
        if token.type == Type.PUSHBYTE:
            pushbyte_token(token, toks)
        if token.type == Type.RETURN:
            return_token(token, toks)
        if token.type == Type.STORE:
            store_token(token, toks)
        if token.type == Type.STOREBYTE:
            storebyte_token(token, toks)
        if token.type == Type.SUBTRACT:
            subtract_token(token, toks)
        if token.type == Type.SYSCALL:
            syscall_token(token, toks)
        if token.type == Type.XOR:
            xor_token(token, toks)

        if token.type == Type.LABEL:
            label_token(token, toks)
        if token.type == Type.LITERAL:
            literal_token(token, toks)
        if token.type == Type.REGISTER:
            register_token(token, toks)
        if token.type == Type.VARIABLE:
            variable_token(token, toks)


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        source = f.readlines()
    lexed = lex(source)
    print(parse(lexed))
