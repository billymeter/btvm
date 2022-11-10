from enum import Enum
from machine import Machine
from stuct import unpack


# TODO: the individual instructions don't need if blocks for the addressing modes because that's all handled in the Instruction constructor. Remove all of that crap to shorten the length of this file.

class AddressMode(Enum):
    REGISTER = 1
    LITERAL = 2
    MEMORY = 3
    NONE = 4


class Opcode(Enum):
    ADD = 1
    SUBTRACT = 2
    MULTIPLY = 3
    DIVIDE = 4
    MODULUS = 5
    AND = 6
    OR = 7
    XOR = 8
    NOT = 9
    SHIFTLEFT = 10
    SHIFTRIGHT = 11
    COMPARE = 12
    JUMP = 13
    JUMPEQ = 14
    JUMPNOTEQ = 15
    JUMPLESS = 16
    JUMPLESSEQ = 17
    JUMPGREATER = 18
    JUMPGREATEREQ = 19
    CALL = 20
    RETURN = 21
    LOAD = 22
    LOADWORD = 23
    LOADBYTE = 24
    STORE = 25
    STOREWORD = 26
    STOREBYTE = 27
    MOVE = 28
    PUSH = 29
    POP = 30
    INPUT = 31
    OUTPUT = 32
    SYSCALL = 33
    NOP = 34
    HALT = 35


class Instruction:
    opcodes = {
        b'Ad': Opcode.ADD,
        b'ad': Opcode.ADD,
        b'aD': Opcode.ADD,
        b'Sb': Opcode.SUBTRACT,
        b'sb': Opcode.SUBTRACT,
        b'sB': Opcode.SUBTRACT,
        b'My': Opcode.MULTIPLY,
        b'my': Opcode.MULTIPLY,
        b'mY': Opcode.MULTIPLY,
        b'Dv': Opcode.DIVIDE,
        b'dv': Opcode.DIVIDE,
        b'dV': Opcode.DIVIDE,
        b'Md': Opcode.MODULUS,
        b'md': Opcode.MODULUS,
        b'mD': Opcode.MODULUS,
        b'An': Opcode.AND,
        b'an': Opcode.AND,
        b'Or': Opcode.OR,
        b'or': Opcode.OR,
        b'Xr': Opcode.XOR,
        b'xr': Opcode.XOR,
        b'Nt': Opcode.NOT,
        b'nt': Opcode.NOT,
        b'Sl': Opcode.SHIFTLEFT,
        b'sl': Opcode.SHIFTLEFT,
        b'Sr': Opcode.SHIFTRIGHT,
        b'sr': Opcode.SHIFTRIGHT,
        b'Cp': Opcode.COMPARE,
        b'cp': Opcode.COMPARE,
        b'Jp': Opcode.JUMP,
        b'jp': Opcode.JUMP,
        b'J=': Opcode.JUMPEQ,
        b'j=': Opcode.JUMPEQ,
        b'J!': Opcode.JUMPNOTEQ,
        b'j!': Opcode.JUMPNOTEQ,
        b'J<': Opcode.JUMPLESS,
        b'j<': Opcode.JUMPLESS,
        b'J{': Opcode.JUMPLESSEQ,
        b'j{': Opcode.JUMPLESSEQ,
        b'J>': Opcode.JUMPGREATER,
        b'j>': Opcode.JUMPGREATER,
        b'J}': Opcode.JUMPGREATEREQ,
        b'j}': Opcode.JUMPGREATEREQ,
        b'Cl': Opcode.CALL,
        b'cl': Opcode.CALL,
        b'RT': Opcode.RETURN,
        b'LM': Opcode.LOAD,
        b'LW': Opcode.LOADWORD,
        b'LB': Opcode.LOADBYTE,
        b'SM': Opcode.STORE,
        b'SW': Opcode.STOREWORD,
        b'SB': Opcode.STOREBYTE,
        b'Mv': Opcode.MOVE,
        b'mv': Opcode.MOVE,
        b'mV': Opcode.MOVE,
        b'Pu': Opcode.PUSH,
        b'pu': Opcode.PUSH,
        b'Po': Opcode.POP,
        b'po': Opcode.POP,
        b'In': Opcode.INPUT,
        b'iN': Opcode.INPUT,
        b'Ot': Opcode.OUTPUT,
        b'ot': Opcode.OUTPUT,
        b'oT': Opcode.OUTPUT,
        b'SY': Opcode.SYSCALL,
        b'NO': Opcode.NOP,
        b'HT': Opcode.HALT,
    }

    opcode_modes = {
        b'Ad': AddressMode.REGISTER,
        b'ad': AddressMode.LITERAL,
        b'aD': AddressMode.MEMORY,
        b'Sb': AddressMode.REGISTER,
        b'sb': AddressMode.LITERAL,
        b'sB': AddressMode.MEMORY,
        b'My': AddressMode.REGISTER,
        b'my': AddressMode.LITERAL,
        b'mY': AddressMode.MEMORY,
        b'Dv': AddressMode.REGISTER,
        b'dv': AddressMode.LITERAL,
        b'dV': AddressMode.MEMORY,
        b'Md': AddressMode.REGISTER,
        b'md': AddressMode.LITERAL,
        b'mD': AddressMode.MEMORY,
        b'An': AddressMode.REGISTER,
        b'an': AddressMode.LITERAL,
        b'Or': AddressMode.REGISTER,
        b'or': AddressMode.LITERAL,
        b'Xr': AddressMode.REGISTER,
        b'xr': AddressMode.LITERAL,
        b'Nt': AddressMode.REGISTER,
        b'nt': AddressMode.LITERAL,
        b'Sl': AddressMode.REGISTER,
        b'sl': AddressMode.LITERAL,
        b'Sr': AddressMode.REGISTER,
        b'sr': AddressMode.LITERAL,
        b'Cp': AddressMode.REGISTER,
        b'cp': AddressMode.LITERAL,
        b'Jp': AddressMode.REGISTER,
        b'jp': AddressMode.LITERAL,
        b'J=': AddressMode.REGISTER,
        b'j=': AddressMode.LITERAL,
        b'J!': AddressMode.REGISTER,
        b'j!': AddressMode.LITERAL,
        b'J<': AddressMode.REGISTER,
        b'j<': AddressMode.LITERAL,
        b'J{': AddressMode.REGISTER,
        b'j{': AddressMode.LITERAL,
        b'J>': AddressMode.REGISTER,
        b'j>': AddressMode.LITERAL,
        b'J}': AddressMode.REGISTER,
        b'j}': AddressMode.LITERAL,
        b'Cl': AddressMode.REGISTER,
        b'cl': AddressMode.LITERAL,
        b'RT': AddressMode.NONE,
        b'LM': AddressMode.MEMORY,
        b'LW': AddressMode.MEMORY,
        b'LB': AddressMode.MEMORY,
        b'SM': AddressMode.MEMORY,
        b'SW': AddressMode.MEMORY,
        b'SB': AddressMode.MEMORY,
        b'Mv': AddressMode.REGISTER,
        b'mv': AddressMode.LITERAL,
        b'mV': AddressMode.MEMORY,
        b'Pu': AddressMode.REGISTER,
        b'pu': AddressMode.LITERAL,
        b'Po': AddressMode.REGISTER,
        b'po': AddressMode.LITERAL,
        b'In': AddressMode.REGISTER,
        b'iN': AddressMode.MEMORY,
        b'Ot': AddressMode.REGISTER,
        b'ot': AddressMode.LITERAL,
        b'oT': AddressMode.MEMORY,
        b'SY': AddressMode.NONE,
        b'NO': AddressMode.NONE,
        b'HT': AddressMode.NONE,
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
        self.opcode = self.opcodes[opcode]
        self.mode = self.opcode_modes[opcode]

        if self.mode == AddressMode.REGISTER:
            # decode the register values for the operands
            self.op1 = self.register_codes[byt[2:4]]
            self.op2 = self.register_codes[byt[4:6]]

        if self.mode == AddressMode.LITERAL:
            self.op1 = self.register_codes[byt[2:4]]
            # unpack the literal value
            self.op2 = unpack('>l', byt[4:8])

        if self.mode == AddressMode.MEMORY:
            self.op1 = self.register_codes[byt[2:4]]
            # unpack memory address and dereference
            self.op2 = self.machine.memory[unpack('>l', byt[4:8])]

        if self.mode == AddressMode.NONE:
            # no processing of operands are needed
            # it's all just padding anyway
            pass

    def execute(self) -> None:
        if self.opcode == Opcode.ADD:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.AND:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.CALL:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.COMPARE:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.DIVIDE:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.HALT:
            self.machine.running = False

        if self.opcode == Opcode.INPUT:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.JUMP:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.JUMPEQ:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.JUMPGREATER:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.JUMPGREATEREQ:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.JUMPLESS:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.JUMPLESSEQ:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.JUMPNOTEQ:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.LOAD:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.LOADWORD:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.LOADBYTE:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.MODULUS:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.MULTIPLY:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.MOVE:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                self.machine.registers[self.op1] = self.op2
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.NOP:
            # nopnopnopnopnop
            pass

        if self.opcode == Opcode.NOT:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.OR:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.OUTPUT:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.POP:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.PUSH:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.RETURN:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.SHIFTLEFT:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.SHIFTRIGHT:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.STORE:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.STOREBYTE:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.STOREWORD:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.SUBTRACT:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass

        if self.opcode == Opcode.SYSCALL:
            pass

        if self.opcode == Opcode.XOR:
            if self.mode == AddressMode.REGISTER:
                pass
            if self.mode == AddressMode.LITERAL:
                pass
            if self.mode == AddressMode.MEMORY:
                pass
            if self.mode == AddressMode.NONE:
                pass
