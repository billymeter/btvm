#!/usr/bin/env python3
"""
the btvm disassembler
"""

from disassembler.disassemble import disassemble
import sys


def main():
    with open(sys.argv[1]) as f:
        program = f.read()
    print(disassemble(program))


if __name__ == "__main__":
    main()
