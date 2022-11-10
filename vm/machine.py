from enum import Enum
from instruction import Instruction
from struct import unpack


# class Register(Enum):
#     R0 = 0
#     R1 = 1
#     R2 = 2
#     R3 = 3
#     R4 = 4
#     R5 = 5
#     R6 = 6
#     R7 = 7
#     RIP = 8
#     RSP = 9
#     RBP = 10
#     RRES = 11
#     RSTATUS = 12
#     RERROR = 13

class Error(Enum):
    # Error codes for the system.
    # TODO: write a function for giving human friendly descriptions of these codes.
    NO_ERROR = 0
    FILE_NOT_FOUND = 1
    NO_PERMISSIONS = 2
    END_OF_FILE = 3
    BAD_FILE_DESCRIPTOR = 4


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
            'rip': unpack('>l', program[4:8])[0],
            'rsp': 0xffff,
            'rbp': self.registers['rsp'],
            'rres': 0,
            'rstatus': {
                'zero': 0,
                'overflow': 0,
                'carry': 0,
            },
            'rerror': 0,
        }

        # machine is running flag
        self.running = False

    def status(self):
        print('registers:')
        for i, r in enumerate(self.r):
            print(f'       r{i}: {self.r[r]}')
        print(f'      rip: {self.rip}')
        print(f'      rsp: {self.rsp}')
        print(f'      rbp: {self.rbp}')
        print(f'     rres: {self.rres}')
        print(f'  rstatus: {self.rstatus}')
        print(f'   rerror: {self.rerror}')

    def execute_instruction(self, instruction):
        pass

    def execute(self):
        self.running = True
        while self.running:
            instruction = Instruction(self.memory[self.rip:self.rip+8], self)
            instruction.execute()
