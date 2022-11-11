from enum import Enum, auto
# from struct import pack as s_pack
from struct import unpack as s_unpack


def unpack(value):
    return s_unpack(">l", value)[0]


class AddressMode(Enum):
    # addressing modes used by the cpu
    LITERAL = auto()
    MEMORY = auto()
    NONE = auto()
    REGISTER = auto()


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


class VMError(Enum):
    # error codes for the system.
    # TODO: write a function for giving human friendly descriptions of these codes.
    NO_ERROR = auto()
    FILE_NOT_FOUND = auto()
    NO_PERMISSIONS = auto()
    END_OF_FILE = auto()
    BAD_FILE_DESCRIPTOR = auto()
