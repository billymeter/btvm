#!/usr/bin/env python3
"""
btvm assembler parser
"""

from lexer import lex, Token, Type
import sys


def add(iter):
    first = next(iter, "end")
    if first.type == Type.REGISTER:
        opcode = b"Ad"
    second = next(iter, "end")
    print(f"{first} {second}")


def variable(iter):
    pass


def parse(tokens):
    toks = iter(tokens)
    while True:
        token = next(toks, "end")
        if token == "end":
            break
        if token.type == Type.ADD:
            add(toks)
        if token.type == Type.VARIABLE:
            variable(toks)


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        source = f.readlines()
    lexed = lex(source)
    print(parse(lexed))
