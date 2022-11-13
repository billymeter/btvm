from util import AddressMode, Opcode, unpack, Register, StatusFlag
import sys


class Machine:
    def __init__(self, program: bytes):
        # create some memory and load the program into it
        self.memory = program + bytearray([0] * (0x10000 - len(program)))

        # set up registers
        self.registers = {
            Register.R0: 0,
            Register.R1: 0,
            Register.R2: 0,
            Register.R3: 0,
            Register.R4: 0,
            Register.R5: 0,
            Register.R6: 0,
            Register.R7: 0,
            Register.RIP: unpack(program[4:8]),
            Register.RSP: 0xffff,
            Register.RBP: 0xffff,
            Register.RRES: 0,
            Register.RERROR: 0,
            Register.RSTATUS: {
                StatusFlag.CARRY: False,
                StatusFlag.OVERFLOW: False,
                StatusFlag.SIGN: False,
                StatusFlag.ZERO: False,
            },
        }

        # machine is running flag
        self.running = False

    def get_status(self, flag: StatusFlag) -> bool:
        return self.registers[Register.RSTATUS][flag]

    def halt(self) -> None:
        self.running = False

    def pop(self, size: int) -> bytes:
        pass

    def push(self, value: bytes, size: int) -> None:
        pass

    def run(self) -> None:
        self.running = True
        while self.running:
            self.step()

    def set_status(self, flag: StatusFlag, value: bool) -> None:
        self.registers[Register.RSTATUS][flag] = value

    def status(self) -> None:
        print('registers:')
        for _, v in enumerate(self.registers):
            if v == Register.RSTATUS:
                for k in self.registers[Register.RSTATUS]:
                    print(f"       {k}: {self.registers[Register.RSTATUS][k]}")
            else:
                print(
                    f'       {v}: {hex(self.registers[v])} ({type(self.registers[v])})')

    def step(self) -> None:
        # fetch and decode instruction
        instruction = Instruction(
            self.memory[self.registers[Register.RIP]: self.registers[Register.RIP]+8], self)

        # advance the instruction pointer
        self.registers[Register.RIP] += 8

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
        b'LB': (Opcode.LOADBYTE, AddressMode.MEMORY),
        # b'LW': (Opcode.LOADWORD, AddressMode.MEMORY),
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
        # b'SW': (Opcode.STOREWORD, AddressMode.MEMORY),
        b'sb': (Opcode.SUBTRACT, AddressMode.LITERAL),
        b'sB': (Opcode.SUBTRACT, AddressMode.MEMORY),
        b'Sb': (Opcode.SUBTRACT, AddressMode.REGISTER),
        b'SY': (Opcode.SYSCALL, AddressMode.NONE),
        b'xr': (Opcode.XOR, AddressMode.LITERAL),
        b'Xr': (Opcode.XOR, AddressMode.REGISTER),
    }

    register_codes = {
        b'r0': Register.R0,
        b'r1': Register.R1,
        b'r2': Register.R2,
        b'r3': Register.R3,
        b'r4': Register.R4,
        b'r5': Register.R5,
        b'r6': Register.R6,
        b'r7': Register.R7,
        b'ip': Register.RIP,
        b'sp': Register.RSP,
        b'bp': Register.RBP,
        b'rs': Register.RRES,
        b'st': Register.RSTATUS,
        b'er': Register.RERROR,
    }

    def __init__(self, byt: bytes, machine: Machine):
        self.machine = machine
        opcode = byt[:2]
        try:
            self.opcode, self.address_mode = self.opcodes[opcode]
        except KeyError as invalid:
            print(f'opcode {invalid} is not a valid opcode!')
            self.machine.running = False

        if AddressMode.REGISTER == self.address_mode:
            # decode the register values for the operands
            self.op1 = self.register_codes[byt[2:4]]
            if b'bt' != byt[4:6]:
                self.op2 = self.register_codes[byt[4:6]]

        if AddressMode.LITERAL == self.address_mode:
            if b'bt' != byt[2:4]:
                self.op1 = self.register_codes[byt[2:4]]
            # unpack the literal value
            self.op2 = unpack(byt[4:8])

        if AddressMode.MEMORY == self.address_mode:
            self.op1 = self.register_codes[byt[2:4]]
            # unpack memory address and dereference
            self.op2 = self.machine.memory[unpack(byt[4:8])]

        if AddressMode.NONE == self.address_mode:
            # no processing of operands are needed
            # it's all just padding anyway
            pass

    def execute(self) -> None:
        if Opcode.ADD == self.opcode:
            # TODO: set overflow/carry flags
            result = self.machine.registers[self.op1] + self.op2
            # detect if the sum is greater than 16 bits and set the flag if so
            self.machine.set_status(
                StatusFlag.CARRY, result & 0xffff == 0 and result & 0x10000)
            self.machine.registers[self.op1] = result & 0xffff

        if Opcode.AND == self.opcode:
            self.machine.registers[self.op1] &= self.op2

        if Opcode.CALL == self.opcode:
            pass

        if Opcode.COMPARE == self.opcode:
            result = self.machine.registers[self.op1] - self.op2
            self.machine.set_status(
                StatusFlag.ZERO, self.machine.registers[self.op1] - self.op2 == 0)
            self.machine.registers[Register.RRES] = result

        if Opcode.DIVIDE == self.opcode:
            # integer division only
            # TODO: set overflow/carry flags
            self.machine.registers[self.op1] //= self.op2

        if Opcode.HALT == self.opcode:
            self.machine.halt()

        if Opcode.INPUT == self.opcode:
            pass

        if Opcode.JUMP == self.opcode:
            self.machine.registers[Register.RIP] = self.op2

        if Opcode.JUMPEQ == self.opcode:
            if self.machine.get_status(StatusFlag.ZERO):
                self.machine.registers[Register.RIP] = self.op2

        if Opcode.JUMPGREATER == self.opcode:
            if self.machine.registers[Register.RRES] > 0:
                self.machine.registers[Register.RIP] = self.op2

        if Opcode.JUMPGREATEREQ == self.opcode:
            if self.machine.registers[Register.RRES] >= 0:
                self.machine.registers[Register.RIP] = self.op2

        if Opcode.JUMPLESS == self.opcode:
            if self.machine.registers[Register.RRES] < 0:
                self.machine.registers[Register.RIP] = self.op2

        if Opcode.JUMPLESSEQ == self.opcode:
            if self.machine.registers[Register.RRES] <= 0:
                self.machine.registers[Register.RIP] = self.op2

        if Opcode.JUMPNOTEQ == self.opcode:
            if not self.machine.get_status(StatusFlag.ZERO):
                self.machine.registers[Register.RIP] = self.op2

        if Opcode.LOAD == self.opcode:
            #hex((0xff << 8)+0x36)
            value = (self.machine.memory[self.op2]
                     << 8) + self.machine.memory[self.op2+1]
            self.machine.registers[self.op1] = value

        # if Opcode.LOADWORD == self.opcode:
        #     pass

        if Opcode.LOADBYTE == self.opcode:
            self.machine.registers[self.op1] = self.machine.memory[self.op2]

        if Opcode.MODULUS == self.opcode:
            self.machine.registers[self.op1] %= self.op2

        if Opcode.MULTIPLY == self.opcode:
            # TODO: overflow and carry flags
            self.machine.registers[self.op1] *= self.op2

        if Opcode.MOVE == self.opcode:
            self.machine.registers[self.op1] = self.op2

        if Opcode.NOP == self.opcode:
            # nopnopnopnopnop
            pass

        if Opcode.NOT == self.opcode:
            self.machine.registers[self.op1] = ~self.machine.registers[self.op1]

        if Opcode.OR == self.opcode:
            self.machine.registers[self.op1] |= self.op2

        if Opcode.OUTPUT == self.opcode:
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

            sys.stdout.write(char)

        if Opcode.POP == self.opcode:
            pass

        if Opcode.POPBYTE == self.opcode:
            pass

        if Opcode.PUSH == self.opcode:
            pass

        if Opcode.PUSHBYTE == self.opcode:
            pass

        if Opcode.RETURN == self.opcode:
            pass

        # if Opcode.SHIFTLEFT == self.opcode:
        #     pass

        # if Opcode.SHIFTRIGHT == self.opcode:
        #     pass

        if Opcode.STORE == self.opcode:
            self.machine.memory[self.op1] = self.op2

        if Opcode.STOREBYTE == self.opcode:
            self.machine.memory[self.op1] = self.op2 & 0xff

        # if Opcode.STOREWORD == self.opcode:
        #     self.machine.memory[self.op1] = self.op2 & 0xffff

        if Opcode.SUBTRACT == self.opcode:
            # TODO: set overflow/carry flags
            self.machine.registers[self.op1] -= self.op2

        if Opcode.SYSCALL == self.opcode:
            pass

        if Opcode.XOR == self.opcode:
            self.machine.registers[self.op1] ^= self.op2
