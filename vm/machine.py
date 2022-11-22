from util import AddressMode
from util import Opcode, opcodes
from util import Register, register_codes
from util import StatusFlag
from util import SystemCall, syscall_table
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
            Register.RIP: int(program[4:8], 16),
            Register.RSP: 0xffff,
            Register.RBP: 0xffff,
            Register.RRES: 0,
            Register.RERROR: 0,
            Register.RSTATUS: 0,
        }

        self.open_file_descriptors: dict()

        # machine is running flag
        self.running = False

    def halt(self) -> None:
        self.running = False

    def pop(self) -> bytes:
        msb = self.popbyte()
        lsb = self.popbyte()
        return (msb >> 8) + lsb

    def popbyte(self) -> bytes:
        value = self.memory[self.registers[Register.RSP]]
        self.registers[Register.RSP] += 1

        if self.registers[Register.RSP] > 0xffff or self.registers[Register.RSP] < 0:
            self.running = False
            raise RuntimeError(
                "stack pointer moved out of bounds! must be between 0 and 0xffff!")
        return value

    def push(self, value: bytes) -> None:
        # have to push these in reverse order since the stack grows down
        lsb = value & 0xff
        self.pushbyte(lsb)
        msb = (value & 0xff00) >> 8
        self.pushbyte(msb)

    def pushbyte(self, value: bytes) -> None:
        self.registers[Register.RSP] -= 1

        if self.registers[Register.RSP] > 0xffff or self.registers[Register.RSP] < 0:
            self.running = False
            raise RuntimeError(
                "stack pointer moved out of bounds! must be between 0 and 0xffff!")
        self.memory[self.registers[Register.RSP]] = value & 0xff

    def run(self) -> None:
        self.running = True
        while self.running:
            self.step()

    def status(self) -> None:
        print('registers:')
        for k, v in self.registers.items():
            print(f'  {k}: {hex(v)}')

    def step(self) -> None:
        # fetch and decode instruction
        instruction = Instruction(
            self.memory[self.registers[Register.RIP]: self.registers[Register.RIP]+8], self)

        # advance the instruction pointer
        self.registers[Register.RIP] += 8

        instruction.execute()

    def systemcall(self, syscall: int, argument_1: int, argument_2: int, argument_3: int, argument_4: int) -> int:
        if SystemCall.EXIT == syscall:
            sys.exit(argument_1)

        if SystemCall.OPEN == syscall:
            pass

        if SystemCall.READ == syscall:
            pass

        if SystemCall.WRITE == syscall:
            pass

        if SystemCall.CLOSE == syscall:
            pass

        if SystemCall.RANDOM == syscall:
            pass


class Instruction:
    def __init__(self, byt: bytes, machine: Machine):
        self.machine = machine
        opcode = byt[:2]
        try:
            self.opcode, self.address_mode = opcodes[opcode]
        except KeyError as invalid:
            print(
                f'opcode {invalid} at address {hex(self.machine.registers[Register.RIP])} is not a valid opcode!')
            print('reg dump:')
            for k, v in self.machine.registers.items():
                print(f'  {k}: {hex(v)}')
            self.machine.running = False

        # set the destination register operand
        self.op1 = register_codes[byt[2:4]]

        # figure out what the second operand should be based
        # on the address mode
        if AddressMode.REGISTER == self.address_mode:
            # decode the register values for the operands
            self.op2 = register_codes[byt[4:6]]

        if AddressMode.REGISTERDEREF == self.address_mode:
            addr = register_codes[byt[4:8]]
            self.op2 = self.machine.memory[addr]

        if AddressMode.LITERAL == self.address_mode:
            self.op2 = int(byt[4:8], 16)

        if AddressMode.MEMORY == self.address_mode:
            # unpack memory address and dereference
            self.op2 = self.machine.memory[int(byt[4:8], 16)]

        if AddressMode.NONE == self.address_mode:
            # no processing of operands are needed
            # it's all just padding anyway
            pass

    def execute(self) -> None:
        if Opcode.ADD == self.opcode:
            self.machine.registers[self.op1] += self.op2 & 0xffff

        if Opcode.AND == self.opcode:
            self.machine.registers[self.op1] &= self.op2

        if Opcode.CALL == self.opcode:
            self.machine.push(self.machine.registers[Register.RIP])
            if self.op1:
                # register
                self.machine.registers[Register.RIP] = self.op1
            else:
                # literal value
                self.machine.registers[Register.RIP] = self.op2

        if Opcode.COMPARE == self.opcode:
            result = self.machine.registers[self.op1] - self.op2
            self.machine.registers[Register.RRES] = result

            if result == 0:
                self.machine.registers[Register.RSTATUS] |= StatusFlag.ZERO

        if Opcode.DIVIDE == self.opcode:
            # integer division only
            self.machine.registers[self.op1] //= self.op2 & 0xffff

        if Opcode.HALT == self.opcode:
            self.machine.halt()

        if Opcode.INPUT == self.opcode:
            self.machine.registers[self.op1] = sys.stdin.read(1)

        if Opcode.JUMP == self.opcode:
            self.machine.registers[Register.RIP] = self.op2

        if Opcode.JUMPEQ == self.opcode:
            if self.machine.registers[Register.RSTATUS] & StatusFlag.ZERO:
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
            if ~self.machine.registers[Register.RSTATUS] & StatusFlag.ZERO:
                self.machine.registers[Register.RIP] = self.op2

        if Opcode.LOAD == self.opcode:
            self.machine.registers[self.op1] = self.op2

        if Opcode.LOADBYTE == self.opcode:
            self.machine.registers[self.op1] = self.machine.memory[self.op2]

        if Opcode.MODULUS == self.opcode:
            self.machine.registers[self.op1] %= self.op2 & 0xffff

        if Opcode.MULTIPLY == self.opcode:
            self.machine.registers[self.op1] *= self.op2 & 0xffff

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
            self.machine.registers[self.op1] = self.machine.pop()

        if Opcode.POPBYTE == self.opcode:
            self.machine.registers[self.op1] = self.machine.popbyte()

        if Opcode.PUSH == self.opcode:
            self.machine.push(self.op1)

        if Opcode.PUSHBYTE == self.opcode:
            self.machine.pushbyte(self.op1)

        if Opcode.RETURN == self.opcode:
            ret = self.machine.pop()
            self.machine.registers[Register.RIP] = ret

        if Opcode.STORE == self.opcode:
            self.machine.memory[self.op1] = self.op2

        if Opcode.STOREBYTE == self.opcode:
            self.machine.memory[self.op1] = self.op2 & 0xff

        if Opcode.SUBTRACT == self.opcode:
            self.machine.registers[self.op1] -= self.op2 & 0xff

        if Opcode.SYSCALL == self.opcode:
            syscall = syscall_table[self.registers[Register.R0]]
            argument_1 = self.registers[Register.R1]
            argument_2 = self.registers[Register.R2]
            argument_3 = self.registers[Register.R3]
            argument_4 = self.registers[Register.R4]
            self.machine.systemcall(syscall=syscall, argument_1=argument_1,
                                    argument_2=argument_2, argument_3=argument_3, argument_4=argument_4)

        if Opcode.XOR == self.opcode:
            self.machine.registers[self.op1] ^= self.op2
