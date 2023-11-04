#!/usr/bin/env python3
"""
the btvm assembler
"""

from assembler.lexer import lex
from assembler.parser import parse
from assembler.assembler import assemble

import os
import shlex
import sys


def flatten(input_list):
    flattened_list = []
    for item in input_list:
        if isinstance(item, list):
            flattened_list.extend(flatten(item))
        else:
            flattened_list.append(item)
    return flattened_list


def resolve_imports(source, path="./"):
    resolved = source
    replacements = []
    for i, line in enumerate(source):
        l = shlex.split(line)

        if l and l[0] == "#include":
            with open(path + "/" + l[1]) as f:
                lines = f.readlines()
            replacements.append((i, lines))

    for i, l in replacements:
        del resolved[i]
        resolved.insert(i, l)

    return flatten(resolved)


def main():
    with open(sys.argv[1]) as f:
        source = f.readlines()
    source = resolve_imports(source, os.path.dirname(sys.argv[1]))
    lexed = lex(source)
    # print(lexed)
    parsed = parse(lexed)
    # print(parsed)
    print(assemble(parsed), end="")


if __name__ == "__main__":
    main()
