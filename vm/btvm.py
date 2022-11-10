#!/usr/bin/env python3
import os
from machine import Machine
from struct import unpack
import sys


with open(sys.argv[1], 'rb') as f:
    program = f.read()

if b'bt_x' != program[:4]:
    print(f'{sys.argv[0]} is not a valid program.')
    os.exit(1)

if len(program) > 0x10000:
    print(
        f'{sys.argv[0]} has a filesize that is too large. unable to run in vm')
    os.exit(1)

vm = Machine(program=program)
vm.status()
