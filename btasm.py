#!/usr/bin/env python3
"""
the btvm assembler
"""

from assembler.lexer import lex
from assembler.parser import parse
from common.common import *
import sys


def main():
    with open(sys.argv[1]) as f:
        source = f.readlines()
    lexed = lex(source)
    print(parse(lexed))


if __name__ == "__main__":
    main()
