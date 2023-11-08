from common.common import *
from time import time
import sys


class Machine:
    def __init__(self, program=bytearray([0] * 0x10000)):
        # create some memory and load the program into it
        self.memory = bytearray(program + bytearray([0] * (0x10000 - len(program))))

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
            Register.RSP: 0xFFFF,
            Register.RBP: 0xFFFF,
            Register.RRES: 0,
            Register.RERROR: 0,
            Register.RCOMPARE: 0,
        }

        self.open_file_descriptors = {0: sys.stdout, 1: sys.stdin, 2: sys.stderr}
        self.files_open = 2

        # machine is running flag
        self.running = False

    def halt(self) -> None:
        self.running = False

    def load_program(self, program):
        self.__init__(program)

    def pop(self):
        msb = self.popbyte()
        lsb = self.popbyte()
        return (msb << 8) + lsb

    def popbyte(self):
        value = self.memory[self.registers[Register.RSP]]
        # if self.registers[Register.RSP] != 0xFFFF:
        self.registers[Register.RSP] += 1

        if self.registers[Register.RSP] > 0x10000 or self.registers[Register.RSP] < 0:
            self.running = False
            raise RuntimeError(
                "stack pointer moved out of bounds! must be between 0 and 0xffff!"
            )
        return value

    def push(self, value: bytes) -> None:
        # have to push these in reverse order since the stack grows down
        lsb = value & 0xFF
        self.pushbyte(lsb)
        msb = (value & 0xFF00) >> 8
        self.pushbyte(msb)

    def pushbyte(self, value: bytes) -> None:
        # if we're at the very top of the stack, don't decrement
        # if self.registers[Register.RSP] != 0xFFFF:
        self.registers[Register.RSP] -= 1
        if self.registers[Register.RSP] > 0x10000 or self.registers[Register.RSP] < 0:
            self.running = False
            raise RuntimeError(
                "stack pointer moved out of bounds! must be between 0 and 0xffff!"
            )
        self.memory[self.registers[Register.RSP]] = int(value) & 0xFF

    def run(self) -> None:
        self.running = True
        while self.running:
            self.step()

    def status(self) -> None:
        print("registers:")
        for k, v in self.registers.items():
            print(f"  {k}: {hex(v)}")

    def step(self) -> None:
        # fetch and decode instruction
        instruction = Instruction(
            self.memory[
                self.registers[Register.RIP] : self.registers[Register.RIP] + 8
            ],
            self,
        )

        # advance the instruction pointer
        self.registers[Register.RIP] += 8

        instruction.execute()

    def systemcall(
        self,
        syscall: int,
        argument_1: int,
        argument_2: int,
        argument_3: int,
        argument_4: int,
    ):
        if SystemCall.EXIT == syscall:
            sys.exit(argument_1)

        if SystemCall.OPEN == syscall:
            # get the path string from memory
            end_point = self.memory.find(b"\\0", argument_1)
            if end_point == -1:
                self.registers[Register.RERROR] = VMError.FILE_NOT_FOUND
                self.registers[Register.RRES] = -1
                return
            path = bytes(self.memory[argument_1:end_point])
            try:
                if isinstance(argument_2, int):
                    if argument_2 == 1:
                        mode = "r"
                    elif argument_2 == 2:
                        mode = "w"
                    else:
                        mode = "r"
                fd = open(path, mode)
                self.files_open += 1
                self.open_file_descriptors[self.files_open] = fd
                self.registers[Register.RERROR] = 0
                self.registers[Register.RRES] = self.files_open
            except FileNotFoundError:
                self.registers[Register.RERROR] = VMError.FILE_NOT_FOUND
                self.registers[Register.RRES] = -1
            except PermissionError:
                self.registers[Register.RERROR] = VMError.NO_PERMISSIONS
                self.registers[Register.RRES] = -1
            return

        if SystemCall.READ == syscall:
            filedes = self.open_file_descriptors[argument_1]
            buf = bytes(filedes.read(argument_3), "utf-8")

            if len(buf) == 0:
                self.registers[Register.RERROR] = VMError.END_OF_FILE
                self.registers[Register.RRES] = -1
                return

            self.memory[argument_2 : argument_2 + len(buf)] = buf
            self.registers[Register.RRES] = len(buf)
            return

        if SystemCall.WRITE == syscall:
            filedes = self.open_file_descriptors[argument_1]
            buf = self.memory[argument_2 : argument_2 + argument_3].decode("utf-8")
            bytes_written = filedes.write(buf)
            self.registers[Register.RRES] = bytes_written
            return

        if SystemCall.CLOSE == syscall:
            try:
                self.open_file_descriptors[argument_1].close()
                del self.open_file_descriptors[argument_1]
                self.registers[Register.RRES] = 0
            except KeyError:
                self.registers[Register.RERROR] = VMError.BAD_FILE_DESCRIPTOR
                self.registers[Register.RRES] = -1
            return

        if SystemCall.RANDOM == syscall:
            try:
                with open("/dev/urandom", "rb") as f:
                    self.registers[Register.RRES] = int(f.read(2).hex(), 16)
                    self.registers[Register.RERROR] = 0
            except:
                self.registers[Register.RRES] = -1
                self.registers[Register.RERROR] = VMError.UNKNOWN
            return


class Instruction:
    def __init__(self, byt: bytes, machine: Machine):
        self.machine = machine
        opcode = bytes(byt[:2])
        try:
            self.opcode, self.address_mode = opcodes[opcode]
        except KeyError as invalid:
            with open(f"crash", "w") as f:
                f.write(
                    f"opcode {invalid} at address {hex(self.machine.registers[Register.RIP])} is not a valid opcode!\n\n"
                )
                f.write("reg dump:\n")
                for k, v in self.machine.registers.items():
                    f.write(f"  {k}: {hex(v)}\n")
                f.write("\n")
                f.write(
                    f"open file descriptors: {self.machine.open_file_descriptors}\n\n"
                )
                f.write("contents of memory:\n")
                for i in range(0, 0xFFFF, 16):
                    f.write(
                        "  {:04x}: {}\n".format(
                            i, self.machine.memory[i : i + 16].hex(sep=" ")
                        )
                    )
            print("segmentation fault. crash file created.")
            sys.exit(1)

        # set the destination register operand
        try:
            self.op1 = register_codes[bytes(byt[2:4])]
        except KeyError:
            print(f"bad register {bytes(byt[2:4])}")
            self.machine.status()
            sys.exit(1)

        # figure out what the second operand should be based
        # on the address mode
        if AddressMode.REGISTER == self.address_mode:
            # decode the register values for the operands
            self.op2 = register_codes[bytes(byt[4:6])]
            # if reg:
            #     self.op2 = self.machine.registers[reg]
            # else:
            #     self.op2 = None
            # print(f"op2 set to {reg}: {self.machine.registers[reg]}")

        if AddressMode.REGISTERDEREF == self.address_mode:
            addr = self.machine.registers[register_codes[bytes(byt[4:6])]]
            msb = self.machine.memory[addr]
            lsb = self.machine.memory[addr + 1]
            self.op2 = (msb << 8) + lsb

        if AddressMode.LITERAL == self.address_mode:
            self.op2 = int(byt[4:8], 16)

        if AddressMode.MEMORY == self.address_mode:
            # unpack memory address and dereference
            msb = self.machine.memory[int(byt[4:8], 16)]
            lsb = self.machine.memory[int(byt[4:8], 16) + 1]
            self.op2 = (msb << 8) + lsb

        if AddressMode.NONE == self.address_mode:
            # no processing of operands are needed
            # it's all just padding anyway
            pass

    def execute(self) -> None:
        if Opcode.ADD == self.opcode:
            self.machine.registers[self.op1] += self.op2 & 0xFFFF

        if Opcode.AND == self.opcode:
            self.machine.registers[self.op1] &= self.op2

        if Opcode.CALL == self.opcode:
            self.machine.push(self.machine.registers[Register.RIP])
            if self.op1:
                self.machine.registers[Register.RIP] = self.op1
            else:
                self.machine.registers[Register.RIP] = self.op2

        if Opcode.COMPARE == self.opcode:
            result = self.machine.registers[self.op1] - self.op2
            self.machine.registers[Register.RCOMPARE] = result

        if Opcode.DIVIDE == self.opcode:
            # integer division only
            self.machine.registers[self.op1] //= self.op2 & 0xFFFF

        if Opcode.HALT == self.opcode:
            self.machine.halt()

        if Opcode.INPUT == self.opcode:
            val = sys.stdin.read(1)
            self.machine.registers[self.op2] = ord(val)

        if Opcode.JUMP == self.opcode:
            self.machine.registers[Register.RIP] = self.op2

        if Opcode.JUMPEQ == self.opcode:
            if self.machine.registers[Register.RCOMPARE] == 0:
                self.machine.registers[Register.RIP] = self.op2

        if Opcode.JUMPGREATER == self.opcode:
            if self.machine.registers[Register.RCOMPARE] > 0:
                self.machine.registers[Register.RIP] = self.op2

        if Opcode.JUMPGREATEREQ == self.opcode:
            if self.machine.registers[Register.RCOMPARE] >= 0:
                self.machine.registers[Register.RIP] = self.op2

        if Opcode.JUMPLESS == self.opcode:
            if self.machine.registers[Register.RCOMPARE] < 0:
                self.machine.registers[Register.RIP] = self.op2

        if Opcode.JUMPLESSEQ == self.opcode:
            if self.machine.registers[Register.RCOMPARE] <= 0:
                self.machine.registers[Register.RIP] = self.op2

        if Opcode.JUMPNOTEQ == self.opcode:
            if self.machine.registers[Register.RCOMPARE] != 0:
                self.machine.registers[Register.RIP] = self.op2

        if Opcode.LOAD == self.opcode:
            self.machine.registers[self.op1] = self.op2

        if Opcode.LOADBYTE == self.opcode:
            self.machine.registers[self.op1] = self.machine.memory[self.op2]

        if Opcode.MODULUS == self.opcode:
            self.machine.registers[self.op1] %= self.op2 & 0xFFFF

        if Opcode.MULTIPLY == self.opcode:
            self.machine.registers[self.op1] *= self.op2 & 0xFFFF

        if Opcode.NOP == self.opcode:
            # nopnopnopnopnop
            pass

        if Opcode.NOT == self.opcode:
            self.machine.registers[self.op1] = ~self.machine.registers[self.op1]

        if Opcode.OR == self.opcode:
            self.machine.registers[self.op1] |= self.op2

        if Opcode.OUTPUT == self.opcode:
            # workaround for dereferences pulling 16-bits and
            # literals only being 8 bits
            if isinstance(self.op2, int):
                if self.op2 > 0xFF:
                    sys.stdout.write(chr(self.op2 >> 8 & 0xFF))
                else:
                    sys.stdout.write(chr(self.op2))
            else:
                sys.stdout.write(chr(self.machine.registers[self.op2]))

        if Opcode.POP == self.opcode:
            self.machine.registers[self.op1] = self.machine.pop()

        if Opcode.POPBYTE == self.opcode:
            self.machine.registers[self.op1] = self.machine.popbyte()

        if Opcode.PUSH == self.opcode:
            self.machine.push(self.op2)

        if Opcode.PUSHBYTE == self.opcode:
            self.machine.pushbyte(self.op2)

        if Opcode.RETURN == self.opcode:
            self.machine.registers[Register.RIP] = self.machine.pop()

        if Opcode.STORE == self.opcode:
            addr = self.machine.registers[self.op1]
            lsb = self.op2 & 0xFF
            msb = (self.op2 >> 8) & 0xFF
            self.machine.memory[addr] = msb
            self.machine.memory[addr + 1] = lsb

        if Opcode.STOREBYTE == self.opcode:
            addr = self.machine.registers[self.op1]
            self.machine.memory[addr] = self.op2 & 0xFF

        if Opcode.SUBTRACT == self.opcode:
            self.machine.registers[self.op1] -= self.op2 & 0xFFFF

        if Opcode.SYSCALL == self.opcode:
            syscall = syscall_table[self.machine.registers[Register.R0]]
            argument_1 = self.machine.registers[Register.R1]
            argument_2 = self.machine.registers[Register.R2]
            argument_3 = self.machine.registers[Register.R3]
            argument_4 = self.machine.registers[Register.R4]
            self.machine.systemcall(
                syscall=syscall,
                argument_1=argument_1,
                argument_2=argument_2,
                argument_3=argument_3,
                argument_4=argument_4,
            )

        if Opcode.XOR == self.opcode:
            self.machine.registers[self.op1] ^= self.op2
