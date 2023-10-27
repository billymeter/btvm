#!/usr/bin/env python3
"""
the btvm assembler
"""

from assembler.lexer import lex
from assembler.parser import parse, symbol_table
from assembler.assembler import assemble
from common.common import *
import sys


def main():
    with open(sys.argv[1]) as f:
        source = f.readlines()
    lexed = lex(source)
    parsed = parse(lexed)
    # print(parsed)
    print(assemble(parsed))


if __name__ == "__main__":
    main()
