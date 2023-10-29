# btvm architecture v0.1

## design goals

- simple architecture for others to learn assembly and basic binary exploitation
- learn architecture design and implementation of an isa
- learn implementation of an assembler, disassembler, c compiler, linker, and debugger
- keep as much of the binary format in printable ascii as possible. this won't always be possible due to addresses won't always have ascii printable values, but modifications to binary programs can become feasible in a text editor rather than someone needing a hex editor
- capital letters only belong in binaries

## general notes

- all opcodes are ascii
- 16-bit arch
- risc
- byte addressable memory
- c-style strings
- big endian
- 64-bit fixed width instructions
- binaries are composed of instructions and data. all data comes after the last instruction
- binary format:
  - magic number (executable or object file; magic numbers: `bt_x` or `bt_o` )
  - instruction entry point (if `bt_x`)
  - metadata: author data, symbol table?
  - start of instructions
  - data
- registers are initialized to zero, except for the stack pointer and base pointer, which are initialized to `0xffff`
- all memory space is initialized to zero, then the program is loaded into memory starting at address 0

## memory map

the memory map is simple. a 256k bank of memory is split in half between the rom for program instructions and the ram.

| start   | end     | purpose |
| ------- | ------- | ------- |
| 0x00000 | 0x1ffff | rom     |
| 0x10000 | 0x3ffff | ram     |

## registers

- status `rstatus`
  - carry, zero, sign, overflow
- error `rerror`
  - contains error code from previously executed syscall
- instruction pointer `rip`
- stack pointer `rsp`
- base pointer `rbp`
- result `rres`
- general purpose:
  - `r0`, `r1`, `r2`, `r3`, `r4`, `r5`, `r6`, `r7`

## opcodes and operands

since each instruction is a fixed width of 64-bits, this allows us to have a 16-bit opcode,
and up to three opcodes of 16-bits each. all operands not used will be `bt` (`0x62 0x74`).

possible combinations:

| form | bits 0 to 15 | 16 to 31 | 32 to 47 | 48 to 64 |
| ---- | ------------ | -------- | -------- | -------- |
| 1    | opcode       | bt       | bt       | bt       |
| 2    | opcode       | operand  | bt       | bt       |
| 3    | opcode       | operand  | operand  | bt       |
| 4    | opcode       | bt       | operand  | operand  |

for example, with an `add` instruction, it can take forms 3 and 4:

form 3: `add r0, r2`

form 4: `add r0, 0x6274, 0x6274`

## instructions

### arithmetic

- add, subtract, multiply, divide, modulus

### boolean

- and, or, xor, not, shl, shr

### comparison, branching, and control flow

- compare, jumpeq, jumpnoteq, jumpless, jumplesseq, jumpgreater, jumpgreatereq
- call, jump, return

### memory load and store operations

load/store a 32-bit value, 16-bit value, or 8-bit value

- load, loadword, loadbyte, store, storeword, storebyte
- move

### stack manipulation

- push, pop

### system instructions

- input, output
- halt, nop, syscall

dword = 32 bits

word = 16 bits

half word = 8 bits

## system calls

system calls each take at most four parameters, with them passed in order in registers r1-r4. syscall
number is stored in r0

- `exit` -- exits the program with a return code
- `open` -- opens a file descriptor
- `read` -- reads from a file descriptor
- `write` -- writes to a file descriptor
- `close` -- closes a file descriptor
- `random` -- system provides a random 16-bit number

### exit `0xa`

`int exit()`

terminates btvm and gives a status code stored in the `rres` register back to the host operating system.

### open `0xb`

`int open(char* path, int mode)`

opens a file descriptor to `path`. returns a file descriptor in `rres` if `rstatus[error]=0`. otherwise, `rres=-1`.

modes:

| mode | value  |
| ---- | ------ |
| 0x1  | read   |
| 0x2  | write  |
| 0x4  | append |

<!-- | 0x8  | binary mode | -->

### read `0xc`

`int read(int filedes, void *buf, uint nbyte)`

reads `nbytes` from `filedes` into `buf`. returns the number of bytes read from `filedes` in `rres`. on error, `rres=-1` and `rerror` is set to the error code.

### write `0xd`

`int write(int filedes, void *buf, uint nbyte)`

writes `nbyte` bytes from `buf` to `filedes`. returns the number of bytes written in `rres`. on error, `rres=-1` and `rerror` is set to the error code.

### close `0xe`

`int close(int filedes)`

closes file descriptor `filedes`. success sets `rres` to `0`. on error `rres` set to `-1` and `rerror` contains error code.

### random `0xf`

`int random()`

generates a random 16-bit number and puts the result in `rres`. `rres` is set to `-1` on error.

### error codes

| code | description         |
| ---- | ------------------- |
| 0    | no error            |
| 1    | file not found      |
| 2    | no permissions      |
| 3    | end of file         |
| 4    | bad file descriptor |

## calling convention

first 4 args in r1-r4. rest are passed on the stack in reverse order like cdecl. callee responsible for saving register values. caller responsible for cleaning up the stack.

## references

thanks to endeav0r for his work on the haxathon supremacy virtual machine which was inspiration for this project. https://github.com/endeav0r/hsvm
