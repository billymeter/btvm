#!/usr/bin/env python3
"""
the btvm virtual machine
"""

from vm.machine import Machine
import sys


with open(sys.argv[1], "rb") as f:
    program = f.read()

if b"bt_x" != program[:4]:
    print(f"{sys.argv[1]} is not a valid program.")
    sys.exit(1)

if len(program) > 0x10000:
    print(f"{sys.argv[1]} has a filesize that is too large. unable to run in vm")
    sys.exit(1)

vm = Machine(program=program)
vm.run()
