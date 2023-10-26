from enum import auto, Enum


class AddressMode(Enum):
    # addressing modes used by the cpu
    LITERAL = auto()
    MEMORY = auto()
    NONE = auto()
    REGISTER = auto()
    REGISTERDEREF = auto()


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
    LOADWORD = auto()
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
    STOREWORD = auto()
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


class FileMode(Enum):
    READ = 0x1
    WRITE = 0x2
    APPEND = 0x4


class VMError(Enum):
    # error codes for the system.
    NO_ERROR = auto()
    FILE_NOT_FOUND = auto()
    NO_PERMISSIONS = auto()
    END_OF_FILE = auto()
    BAD_FILE_DESCRIPTOR = auto()
    UNKNOWN = auto()


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
    b"an": (Opcode.AND, AddressMode.LITERAL),
    b"An": (Opcode.AND, AddressMode.REGISTER),
    b"cl": (Opcode.CALL, AddressMode.LITERAL),
    b"Cl": (Opcode.CALL, AddressMode.REGISTER),
    b"cp": (Opcode.COMPARE, AddressMode.LITERAL),
    b"Cp": (Opcode.COMPARE, AddressMode.REGISTER),
    b"CP": (Opcode.COMPARE, AddressMode.REGISTERDEREF),
    b"dv": (Opcode.DIVIDE, AddressMode.LITERAL),
    b"dV": (Opcode.DIVIDE, AddressMode.MEMORY),
    b"Dv": (Opcode.DIVIDE, AddressMode.REGISTER),
    b"HT": (Opcode.HALT, AddressMode.NONE),
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
    b"my": (Opcode.MULTIPLY, AddressMode.LITERAL),
    b"mY": (Opcode.MULTIPLY, AddressMode.MEMORY),
    b"My": (Opcode.MULTIPLY, AddressMode.REGISTER),
    b"NO": (Opcode.NOP, AddressMode.NONE),
    b"nt": (Opcode.NOT, AddressMode.LITERAL),
    b"Nt": (Opcode.NOT, AddressMode.REGISTER),
    b"or": (Opcode.OR, AddressMode.LITERAL),
    b"Or": (Opcode.OR, AddressMode.REGISTER),
    b"ot": (Opcode.OUTPUT, AddressMode.LITERAL),
    b"oT": (Opcode.OUTPUT, AddressMode.MEMORY),
    b"Ot": (Opcode.OUTPUT, AddressMode.REGISTER),
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
    b"SC": (Opcode.SYSCALL, AddressMode.NONE),
    b"xr": (Opcode.XOR, AddressMode.LITERAL),
    b"Xr": (Opcode.XOR, AddressMode.REGISTER),
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
    b"st": Register.RSTATUS,
    b"er": Register.RERROR,
}


syscall_table = {
    b"a": SystemCall.EXIT,
    b"b": SystemCall.OPEN,
    b"c": SystemCall.READ,
    b"d": SystemCall.WRITE,
    b"e": SystemCall.CLOSE,
    b"f": SystemCall.RANDOM,
}
