#!/usr/bin/env python3
"""
btvm assembler lexer
"""

from common.common import *
import shlex
import sys


def lex_word(word, line_num):
    lword = word.lower()
    if "add" == lword:
        return Token(Type.ADD, None, line_num)
    if "and" == lword:
        return Token(Type.AND, None, line_num)
    if "call" == lword:
        return Token(Type.CALL, None, line_num)
    if "compare" == lword:
        return Token(Type.COMPARE, None, line_num)
    if "divide" == lword:
        return Token(Type.DIVIDE, None, line_num)
    if "halt" == lword:
        return Token(Type.HALT, None, line_num)
    if "input" == lword:
        return Token(Type.INPUT, None, line_num)
    if "jump" == lword:
        return Token(Type.JUMP, None, line_num)
    if "jumpeq" == lword:
        return Token(Type.JUMPEQ, None, line_num)
    if "jumpgreater" == lword:
        return Token(Type.JUMPGREATER, None, line_num)
    if "jumpgreatereq" == lword:
        return Token(Type.JUMPGREATEREQ, None, line_num)
    if "jumpless" == lword:
        return Token(Type.JUMPLESS, None, line_num)
    if "jumplesseq" == lword:
        return Token(Type.JUMPLESSEQ, None, line_num)
    if "jumpnoteq" == lword:
        return Token(Type.JUMPNOTEQ, None, line_num)
    if "load" == lword:
        return Token(Type.LOAD, None, line_num)
    if "loadbyte" == lword:
        return Token(Type.LOADBYTE, None, line_num)
    if "modulus" == lword:
        return Token(Type.MODULUS, None, line_num)
    if "multiply" == lword:
        return Token(Type.MULTIPLY, None, line_num)
    if "nop" == lword:
        return Token(Type.NOP, None, line_num)
    if "not" == lword:
        return Token(Type.NOT, None, line_num)
    if "or" == lword:
        return Token(Type.OR, None, line_num)
    if "output" == lword:
        return Token(Type.OUTPUT, None, line_num)
    if "pop" == lword:
        return Token(Type.POP, None, line_num)
    if "popbyte" == lword:
        return Token(Type.POPBYTE, None, line_num)
    if "push" == lword:
        return Token(Type.PUSH, None, line_num)
    if "pushbyte" == lword:
        return Token(Type.PUSHBYTE, None, line_num)
    if "return" == lword:
        return Token(Type.RETURN, None, line_num)
    if "store" == lword:
        return Token(Type.STORE, None, line_num)
    if "storebyte" == lword:
        return Token(Type.STOREBYTE, None, line_num)
    if "subtract" == lword:
        return Token(Type.SUBTRACT, None, line_num)
    if "syscall" == lword:
        return Token(Type.SYSCALL, None, line_num)
    if "xor" == lword:
        return Token(Type.XOR, None, line_num)

    # handle registers
    if lword in {
        "r0",
        "r1",
        "r2",
        "r3",
        "r4",
        "r5",
        "r6",
        "r7",
    }:
        return Token(Type.REGISTER, lword, line_num)
    elif lword == "rip":
        return Token(Type.REGISTER, "ip", line_num)
    elif lword == "rsp":
        return Token(Type.REGISTER, "sp", line_num)
    elif lword == "rbp":
        return Token(Type.REGISTER, "bp", line_num)
    elif lword == "rres":
        return Token(Type.REGISTER, "rs", line_num)
    elif lword == "rerror":
        return Token(Type.REGISTER, "er", line_num)

    # handle variables
    if word.startswith(".") and word.endswith(":"):
        return Token(Type.VARIABLE, word[1:-1], line_num)

    # handle labels
    if word.endswith(":"):
        return Token(Type.LABEL, word[:-1], line_num)

    # handle dereferences
    if word.startswith("[") and word.endswith("]"):
        try:
            if lword[1:3] == "0x":
                val = int(word[1:-1], 16)
            else:
                val = int(word[1:-1])
        except:
            val = word[1:-1]
        return Token(Type.DEREF, val, line_num)

    # handle literals
    try:
        if lword[:2] == "0x":
            val = int(word[2:], 16)
        else:
            val = int(word)
    except:
        val = word

    return Token(Type.LITERAL, val, line_num)


def lex_line(line, line_num):
    tokens = []
    # shlex.split is used to help us with quoted strings
    # https://stackoverflow.com/questions/79968/split-a-string-by-spaces-preserving-quoted-substrings-in-python
    for word in shlex.split(line):
        tokens.append(lex_word(word, line_num))
    return tokens


def lex(source):
    tokens = []
    line_num = 1

    for line in source:
        # check if the line is empty
        if not line:
            line_num += 1
            continue
        # lex the line, while stripping out comments
        # and extra white space
        toks = lex_line(line.split(";")[0].strip(), line_num)
        tokens.extend(toks)
        line_num += 1
    return tokens


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        source = f.readlines()
    lexed = lex(source)

    last_line = 1
    for token in lexed:
        if token.line_num != last_line:
            print()
            last_line = token.line_num
        print(token, end=", ")
