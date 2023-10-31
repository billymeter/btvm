from enum import auto, Enum, IntEnum


class AddressMode(Enum):
    # addressing modes used by the cpu
    LITERAL = auto()
    MEMORY = auto()
    NONE = auto()
    REGISTER = auto()
    REGISTERDEREF = auto()


class FileMode(Enum):
    READ = 0x1
    WRITE = 0x2
    APPEND = 0x4


class Node:
    def __init__(
        self, opcode=None, address_mode=None, op1=None, op2=None, resolve_symbol=False
    ):
        self.opcode = opcode
        self.address_mode = address_mode
        self.op1 = op1
        self.op2 = op2
        self.resolve_symbol = resolve_symbol

    def __repr__(self):
        return f"{self.opcode} {self.address_mode} {self.op1} {self.op2} {self.resolve_symbol}"


class Opcode(Enum):
    # opcodes for the vm
    ADD = auto()
    AND = auto()
    CALL = auto()
    COMPARE = auto()
    DIVIDE = auto()
    HALT = auto()
    INPUT = auto()
    JUMP = auto()
    JUMPEQ = auto()
    JUMPGREATER = auto()
    JUMPGREATEREQ = auto()
    JUMPLESS = auto()
    JUMPLESSEQ = auto()
    JUMPNOTEQ = auto()
    LOAD = auto()
    LOADBYTE = auto()
    MODULUS = auto()
    MOVE = auto()
    MULTIPLY = auto()
    NOP = auto()
    NOT = auto()
    OR = auto()
    OUTPUT = auto()
    POP = auto()
    POPBYTE = auto()
    PUSH = auto()
    PUSHBYTE = auto()
    RETURN = auto()
    SHIFTLEFT = auto()
    SHIFTRIGHT = auto()
    STORE = auto()
    STOREBYTE = auto()
    SUBTRACT = auto()
    SYSCALL = auto()
    XOR = auto()
    NONE = auto()


class Register(Enum):
    R0 = auto()
    R1 = auto()
    R2 = auto()
    R3 = auto()
    R4 = auto()
    R5 = auto()
    R6 = auto()
    R7 = auto()
    RIP = auto()
    RSP = auto()
    RBP = auto()
    RRES = auto()
    RSTATUS = auto()
    RERROR = auto()


class SystemCall(Enum):
    EXIT = auto()
    OPEN = auto()
    READ = auto()
    WRITE = auto()
    CLOSE = auto()
    RANDOM = auto()


class Token:
    def __init__(self, type, value, line_num):
        self.type = type
        self.value = value
        self.line_num = line_num

    def __str__(self):
        return f"{self.line_num}:{self.type}: {self.value}"

    def __repr__(self):
        return f"{self.line_num}:{self.type}: {self.value}"


class Type(Enum):
    ADD = auto()
    AND = auto()
    CALL = auto()
    COMPARE = auto()
    DIVIDE = auto()
    HALT = auto()
    INPUT = auto()
    JUMP = auto()
    JUMPEQ = auto()
    JUMPGREATER = auto()
    JUMPGREATEREQ = auto()
    JUMPLESS = auto()
    JUMPLESSEQ = auto()
    JUMPNOTEQ = auto()
    LOAD = auto()
    LOADBYTE = auto()
    MODULUS = auto()
    MULTIPLY = auto()
    NOP = auto()
    NOT = auto()
    OR = auto()
    OUTPUT = auto()
    POP = auto()
    POPBYTE = auto()
    PUSH = auto()
    PUSHBYTE = auto()
    RETURN = auto()
    STORE = auto()
    STOREBYTE = auto()
    SUBTRACT = auto()
    SYSCALL = auto()
    XOR = auto()

    DEREF = auto()
    LABEL = auto()
    LITERAL = auto()
    REGISTER = auto()
    VARIABLE = auto()


class VMError(IntEnum):
    # error codes for the system.
    NO_ERROR = 0
    FILE_NOT_FOUND = 1
    NO_PERMISSIONS = 2
    END_OF_FILE = 3
    BAD_FILE_DESCRIPTOR = 4
    UNKNOWN = 5


def error_description(error_num):
    if error_num == VMError.NO_ERROR:
        return "no error"
    if error_num == VMError.FILE_NOT_FOUND:
        return "file not found"
    if error_num == VMError.NO_PERMISSIONS:
        return "insufficient permissions"
    if error_num == VMError.END_OF_FILE:
        return "end of file"
    if error_num == VMError.BAD_FILE_DESCRIPTOR:
        return "invalid file descriptor"


opcodes = {
    b"ad": (Opcode.ADD, AddressMode.LITERAL),
    b"aD": (Opcode.ADD, AddressMode.MEMORY),
    b"Ad": (Opcode.ADD, AddressMode.REGISTER),
    b"AD": (Opcode.ADD, AddressMode.REGISTERDEREF),
    b"an": (Opcode.AND, AddressMode.LITERAL),
    b"aN": (Opcode.AND, AddressMode.MEMORY),
    b"An": (Opcode.AND, AddressMode.REGISTER),
    b"AN": (Opcode.AND, AddressMode.REGISTERDEREF),
    b"cl": (Opcode.CALL, AddressMode.LITERAL),
    b"cL": (Opcode.CALL, AddressMode.MEMORY),
    b"Cl": (Opcode.CALL, AddressMode.REGISTER),
    b"CL": (Opcode.CALL, AddressMode.REGISTERDEREF),
    b"cp": (Opcode.COMPARE, AddressMode.LITERAL),
    b"cP": (Opcode.COMPARE, AddressMode.MEMORY),
    b"Cp": (Opcode.COMPARE, AddressMode.REGISTER),
    b"CP": (Opcode.COMPARE, AddressMode.REGISTERDEREF),
    b"dv": (Opcode.DIVIDE, AddressMode.LITERAL),
    b"dV": (Opcode.DIVIDE, AddressMode.MEMORY),
    b"Dv": (Opcode.DIVIDE, AddressMode.REGISTER),
    b"DV": (Opcode.DIVIDE, AddressMode.REGISTERDEREF),
    b"HT": (Opcode.HALT, AddressMode.NONE),
    b"in": (Opcode.INPUT, AddressMode.LITERAL),
    b"iN": (Opcode.INPUT, AddressMode.MEMORY),
    b"In": (Opcode.INPUT, AddressMode.REGISTER),
    b"IN": (Opcode.INPUT, AddressMode.REGISTERDEREF),
    b"jp": (Opcode.JUMP, AddressMode.LITERAL),
    b"Jp": (Opcode.JUMP, AddressMode.REGISTER),
    b"j=": (Opcode.JUMPEQ, AddressMode.LITERAL),
    b"J=": (Opcode.JUMPEQ, AddressMode.REGISTER),
    b"j>": (Opcode.JUMPGREATER, AddressMode.LITERAL),
    b"J>": (Opcode.JUMPGREATER, AddressMode.REGISTER),
    b"j}": (Opcode.JUMPGREATEREQ, AddressMode.LITERAL),
    b"J}": (Opcode.JUMPGREATEREQ, AddressMode.REGISTER),
    b"j<": (Opcode.JUMPLESS, AddressMode.LITERAL),
    b"J<": (Opcode.JUMPLESS, AddressMode.REGISTER),
    b"j{": (Opcode.JUMPLESSEQ, AddressMode.LITERAL),
    b"J{": (Opcode.JUMPLESSEQ, AddressMode.REGISTER),
    b"j!": (Opcode.JUMPNOTEQ, AddressMode.LITERAL),
    b"J!": (Opcode.JUMPNOTEQ, AddressMode.REGISTER),
    b"ld": (Opcode.LOAD, AddressMode.LITERAL),
    b"lD": (Opcode.LOAD, AddressMode.MEMORY),
    b"Ld": (Opcode.LOAD, AddressMode.REGISTER),
    b"LD": (Opcode.LOAD, AddressMode.REGISTERDEREF),
    b"lb": (Opcode.LOADBYTE, AddressMode.LITERAL),
    b"lB": (Opcode.LOADBYTE, AddressMode.MEMORY),
    b"Lb": (Opcode.LOADBYTE, AddressMode.REGISTER),
    b"LB": (Opcode.LOADBYTE, AddressMode.REGISTERDEREF),
    b"md": (Opcode.MODULUS, AddressMode.LITERAL),
    b"mD": (Opcode.MODULUS, AddressMode.MEMORY),
    b"Md": (Opcode.MODULUS, AddressMode.REGISTER),
    b"MD": (Opcode.MODULUS, AddressMode.REGISTERDEREF),
    b"my": (Opcode.MULTIPLY, AddressMode.LITERAL),
    b"mY": (Opcode.MULTIPLY, AddressMode.MEMORY),
    b"My": (Opcode.MULTIPLY, AddressMode.REGISTER),
    b"MY": (Opcode.MULTIPLY, AddressMode.REGISTERDEREF),
    b"NP": (Opcode.NOP, AddressMode.NONE),
    b"nt": (Opcode.NOT, AddressMode.LITERAL),
    b"nT": (Opcode.NOT, AddressMode.MEMORY),
    b"Nt": (Opcode.NOT, AddressMode.REGISTER),
    b"NT": (Opcode.NOT, AddressMode.REGISTERDEREF),
    b"or": (Opcode.OR, AddressMode.LITERAL),
    b"oR": (Opcode.OR, AddressMode.MEMORY),
    b"Or": (Opcode.OR, AddressMode.REGISTER),
    b"OR": (Opcode.OR, AddressMode.REGISTERDEREF),
    b"ot": (Opcode.OUTPUT, AddressMode.LITERAL),
    b"oT": (Opcode.OUTPUT, AddressMode.MEMORY),
    b"Ot": (Opcode.OUTPUT, AddressMode.REGISTER),
    b"OT": (Opcode.OUTPUT, AddressMode.REGISTERDEREF),
    b"po": (Opcode.POP, AddressMode.LITERAL),
    b"Po": (Opcode.POP, AddressMode.REGISTER),
    b"pb": (Opcode.POPBYTE, AddressMode.LITERAL),
    b"Pb": (Opcode.POPBYTE, AddressMode.REGISTER),
    b"pu": (Opcode.PUSH, AddressMode.LITERAL),
    b"Pu": (Opcode.PUSH, AddressMode.REGISTER),
    b"py": (Opcode.PUSHBYTE, AddressMode.LITERAL),
    b"Py": (Opcode.PUSHBYTE, AddressMode.REGISTER),
    b"RT": (Opcode.RETURN, AddressMode.NONE),
    b"sr": (Opcode.STORE, AddressMode.LITERAL),
    b"Sr": (Opcode.STORE, AddressMode.REGISTER),
    b"sy": (Opcode.STOREBYTE, AddressMode.MEMORY),
    b"Sy": (Opcode.STOREBYTE, AddressMode.REGISTER),
    b"sb": (Opcode.SUBTRACT, AddressMode.LITERAL),
    b"sB": (Opcode.SUBTRACT, AddressMode.MEMORY),
    b"Sb": (Opcode.SUBTRACT, AddressMode.REGISTER),
    b"SB": (Opcode.SUBTRACT, AddressMode.REGISTERDEREF),
    b"SC": (Opcode.SYSCALL, AddressMode.NONE),
    b"xr": (Opcode.XOR, AddressMode.LITERAL),
    b"xR": (Opcode.XOR, AddressMode.MEMORY),
    b"Xr": (Opcode.XOR, AddressMode.REGISTER),
    b"XR": (Opcode.XOR, AddressMode.REGISTERDEREF),
}

register_codes = {
    b"bt": None,
    b"r0": Register.R0,
    b"r1": Register.R1,
    b"r2": Register.R2,
    b"r3": Register.R3,
    b"r4": Register.R4,
    b"r5": Register.R5,
    b"r6": Register.R6,
    b"r7": Register.R7,
    b"ip": Register.RIP,
    b"sp": Register.RSP,
    b"bp": Register.RBP,
    b"rs": Register.RRES,
    b"er": Register.RERROR,
}


syscall_table = {
    0xA: SystemCall.EXIT,
    0xB: SystemCall.OPEN,
    0xC: SystemCall.READ,
    0xD: SystemCall.WRITE,
    0xE: SystemCall.CLOSE,
    0xF: SystemCall.RANDOM,
}
