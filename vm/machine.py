from util import AddressMode, Opcode, unpack
# import sys


class Machine:
    def __init__(self, program):
        if b'bt_x' != program[:4]:
            raise 'not a valid program!'

        # create some memory and load the program into it
        self.memory = program + bytearray([0] * (0x10000 - len(program)))

        # set up registers
        self.registers = {
            'r0': 0,
            'r1': 0,
            'r2': 0,
            'r3': 0,
            'r4': 0,
            'r5': 0,
            'r6': 0,
            'r7': 0,
            'rip': unpack(program[4:8]),
            'rsp': 0xffff,
            'rres': 0,
            'rstatus': {
                'zero': False,
                'overflow': False,
                'carry': False,
            },
            'rerror': 0,
        }
        self.registers['rbp'] = self.registers['rsp']

        # machine is running flag
        self.running = False

    def status(self):
        print('registers:')
        for _, v in enumerate(self.registers):
            if v == 'rstatus':
                for k in self.registers['rstatus']:
                    print(f"       {k}: {self.registers['rstatus'][k]}")
            else:
                print(
                    f'       {v}: {hex(self.registers[v])} ({type(self.registers[v])})')

    def execute_instruction(self, instruction):
        pass

    def execute(self):
        self.running = True
        while self.running:
            # fetch and decode instruction
            instruction = Instruction(
                self.memory[self.registers['rip']: self.registers['rip']+8], self)

            # advance the instruction pointer
            self.registers['rip'] += 8

            instruction.execute()


class Instruction:
    opcodes = {
        b'ad': (Opcode.ADD, AddressMode.LITERAL),
        b'aD': (Opcode.ADD, AddressMode.MEMORY),
        b'Ad': (Opcode.ADD, AddressMode.REGISTER),
        b'an': (Opcode.AND, AddressMode.LITERAL),
        b'An': (Opcode.AND, AddressMode.REGISTER),
        b'cl': (Opcode.CALL, AddressMode.LITERAL),
        b'Cl': (Opcode.CALL, AddressMode.REGISTER),
        b'cp': (Opcode.COMPARE, AddressMode.LITERAL),
        b'Cp': (Opcode.COMPARE, AddressMode.REGISTER),
        b'dv': (Opcode.DIVIDE, AddressMode.LITERAL),
        b'dV': (Opcode.DIVIDE, AddressMode.MEMORY),
        b'Dv': (Opcode.DIVIDE, AddressMode.REGISTER),
        b'HT': (Opcode.HALT, AddressMode.NONE),
        b'iN': (Opcode.INPUT, AddressMode.MEMORY),
        b'In': (Opcode.INPUT, AddressMode.REGISTER),
        b'jp': (Opcode.JUMP, AddressMode.LITERAL),
        b'Jp': (Opcode.JUMP, AddressMode.REGISTER),
        b'j=': (Opcode.JUMPEQ, AddressMode.LITERAL),
        b'J=': (Opcode.JUMPEQ, AddressMode.REGISTER),
        b'j>': (Opcode.JUMPGREATER, AddressMode.LITERAL),
        b'J>': (Opcode.JUMPGREATER, AddressMode.REGISTER),
        b'j}': (Opcode.JUMPGREATEREQ, AddressMode.LITERAL),
        b'J}': (Opcode.JUMPGREATEREQ, AddressMode.REGISTER),
        b'j<': (Opcode.JUMPLESS, AddressMode.LITERAL),
        b'J<': (Opcode.JUMPLESS, AddressMode.REGISTER),
        b'j{': (Opcode.JUMPLESSEQ, AddressMode.LITERAL),
        b'J{': (Opcode.JUMPLESSEQ, AddressMode.REGISTER),
        b'j!': (Opcode.JUMPNOTEQ, AddressMode.LITERAL),
        b'J!': (Opcode.JUMPNOTEQ, AddressMode.REGISTER),
        b'LM': (Opcode.LOAD, AddressMode.MEMORY),
        b'LW': (Opcode.LOADWORD, AddressMode.MEMORY),
        b'LB': (Opcode.LOADBYTE, AddressMode.MEMORY),
        b'md': (Opcode.MODULUS, AddressMode.LITERAL),
        b'mD': (Opcode.MODULUS, AddressMode.MEMORY),
        b'Md': (Opcode.MODULUS, AddressMode.REGISTER),
        b'mv': (Opcode.MOVE, AddressMode.LITERAL),
        b'mV': (Opcode.MOVE, AddressMode.MEMORY),
        b'Mv': (Opcode.MOVE, AddressMode.REGISTER),
        b'my': (Opcode.MULTIPLY, AddressMode.LITERAL),
        b'mY': (Opcode.MULTIPLY, AddressMode.MEMORY),
        b'My': (Opcode.MULTIPLY, AddressMode.REGISTER),
        b'NO': (Opcode.NOP, AddressMode.NONE),
        b'nt': (Opcode.NOT, AddressMode.LITERAL),
        b'Nt': (Opcode.NOT, AddressMode.REGISTER),
        b'or': (Opcode.OR, AddressMode.LITERAL),
        b'Or': (Opcode.OR, AddressMode.REGISTER),
        b'ot': (Opcode.OUTPUT, AddressMode.LITERAL),
        b'oT': (Opcode.OUTPUT, AddressMode.MEMORY),
        b'Ot': (Opcode.OUTPUT, AddressMode.REGISTER),
        b'po': (Opcode.POP, AddressMode.LITERAL),
        b'Po': (Opcode.POP, AddressMode.REGISTER),
        b'pb': (Opcode.POPBYTE, AddressMode.LITERAL),
        b'Pb': (Opcode.POPBYTE, AddressMode.REGISTER),
        b'pu': (Opcode.PUSH, AddressMode.LITERAL),
        b'Pu': (Opcode.PUSH, AddressMode.REGISTER),
        b'py': (Opcode.PUSHBYTE, AddressMode.LITERAL),
        b'Py': (Opcode.PUSHBYTE, AddressMode.REGISTER),
        b'RT': (Opcode.RETURN, AddressMode.NONE),
        b'sl': (Opcode.SHIFTLEFT, AddressMode.LITERAL),
        b'Sl': (Opcode.SHIFTLEFT, AddressMode.REGISTER),
        b'sr': (Opcode.SHIFTRIGHT, AddressMode.LITERAL),
        b'Sr': (Opcode.SHIFTRIGHT, AddressMode.REGISTER),
        b'SM': (Opcode.STORE, AddressMode.MEMORY),
        b'SB': (Opcode.STOREBYTE, AddressMode.MEMORY),
        b'SW': (Opcode.STOREWORD, AddressMode.MEMORY),
        b'sb': (Opcode.SUBTRACT, AddressMode.LITERAL),
        b'sB': (Opcode.SUBTRACT, AddressMode.MEMORY),
        b'Sb': (Opcode.SUBTRACT, AddressMode.REGISTER),
        b'SY': (Opcode.SYSCALL, AddressMode.NONE),
        b'xr': (Opcode.XOR, AddressMode.LITERAL),
        b'Xr': (Opcode.XOR, AddressMode.REGISTER),
    }

    register_codes = {
        b'r0': 'r0',
        b'r1': 'r1',
        b'r2': 'r2',
        b'r3': 'r3',
        b'r4': 'r4',
        b'r5': 'r5',
        b'r6': 'r6',
        b'r7': 'r7',
        b'ip': 'rip',
        b'sp': 'rsp',
        b'bp': 'rbp',
        b'rs': 'rres',
        b'st': 'rstatus',
        b'er': 'rerror'
    }

    def __init__(self, byt: bytes, machine: Machine):
        self.machine = machine
        opcode = byt[:2]
        self.opcode, self.address_mode = self.opcodes[opcode]

        if self.address_mode == AddressMode.REGISTER:
            # decode the register values for the operands
            self.op1 = self.register_codes[byt[2:4]]
            if b'bt' != byt[4:6]:
                self.op2 = self.register_codes[byt[4:6]]

        if self.address_mode == AddressMode.LITERAL:
            self.op1 = self.register_codes[byt[2:4]]
            # unpack the literal value
            self.op2 = unpack(byt[4:8])

        if self.address_mode == AddressMode.MEMORY:
            self.op1 = self.register_codes[byt[2:4]]
            # unpack memory address and dereference
            self.op2 = self.machine.memory[unpack(byt[4:8])]

        if self.address_mode == AddressMode.NONE:
            # no processing of operands are needed
            # it's all just padding anyway
            pass

    def execute(self) -> None:
        if self.opcode == Opcode.ADD:
            # TODO: set overflow/carry flags
            self.machine.registers[self.op1] += self.op2

        if self.opcode == Opcode.AND:
            pass

        if self.opcode == Opcode.CALL:
            pass

        if self.opcode == Opcode.COMPARE:

            self.machine.registers['rstatus']['zero'] = self.machine.registers[self.op1] - \
                self.op2 == 0

        if self.opcode == Opcode.DIVIDE:
            pass

        if self.opcode == Opcode.HALT:
            self.machine.running = False

        if self.opcode == Opcode.INPUT:
            pass

        if self.opcode == Opcode.JUMP:
            pass

        if self.opcode == Opcode.JUMPEQ:
            pass

        if self.opcode == Opcode.JUMPGREATER:
            pass

        if self.opcode == Opcode.JUMPGREATEREQ:
            pass

        if self.opcode == Opcode.JUMPLESS:
            pass

        if self.opcode == Opcode.JUMPLESSEQ:
            pass

        if self.opcode == Opcode.JUMPNOTEQ:
            if not self.machine.registers['rstatus']['zero']:
                self.machine.registers['rip'] = self.op2

        if self.opcode == Opcode.LOAD:
            pass

        if self.opcode == Opcode.LOADWORD:
            pass

        if self.opcode == Opcode.LOADBYTE:
            pass

        if self.opcode == Opcode.MODULUS:
            pass

        if self.opcode == Opcode.MULTIPLY:
            pass

        if self.opcode == Opcode.MOVE:
            self.machine.registers[self.op1] = self.op2

        if self.opcode == Opcode.NOP:
            # nopnopnopnopnop
            pass

        if self.opcode == Opcode.NOT:
            pass

        if self.opcode == Opcode.OR:
            pass

        if self.opcode == Opcode.OUTPUT:
            # this instruction is a little weird
            if self.address_mode == AddressMode.LITERAL:
                # take the least significant byte of the register value
                char = chr(self.machine.registers[self.op1] & 0xff)

            if self.address_mode == AddressMode.REGISTER:
                # dereference value stored in the register
                char = chr(
                    self.machine.memory[self.machine.registers[self.op1]])

            if self.address_mode == AddressMode.MEMORY:
                # output the value at the address in the operand
                char = chr(
                    self.machine.memory[self.machine.registers[self.op2]])

            print(f'{char}', end='')

        if self.opcode == Opcode.POP:
            pass

        if self.opcode == Opcode.POPBYTE:
            pass

        if self.opcode == Opcode.PUSH:
            pass

        if self.opcode == Opcode.PUSHBYTE:
            pass

        if self.opcode == Opcode.RETURN:
            pass

        if self.opcode == Opcode.SHIFTLEFT:
            pass

        if self.opcode == Opcode.SHIFTRIGHT:
            pass

        if self.opcode == Opcode.STORE:
            pass

        if self.opcode == Opcode.STOREBYTE:
            pass

        if self.opcode == Opcode.STOREWORD:
            pass

        if self.opcode == Opcode.SUBTRACT:
            pass

        if self.opcode == Opcode.SYSCALL:
            pass

        if self.opcode == Opcode.XOR:
            pass
