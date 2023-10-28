#!/usr/bin/env python3
"""
btvm assembler parser
"""

from common.common import *
import sys

symbol_table = {}
errors = []


def add_token(token, iter):
    try:
        op1 = next(iter)
        op2 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. add instruction requires two operands."
        )
        return None

    # first operand must be a register
    if op1.type != Type.REGISTER:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to add instruction must be a register."
        )
        return None
    if op2.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op2.type == Type.LITERAL and isinstance(op2.value, int):
        mode = AddressMode.LITERAL
    elif op2.type == Type.DEREF and isinstance(op2.value, int):
        mode = AddressMode.MEMORY
    elif op2.type == Type.DEREF:
        mode = AddressMode.REGISTERDEREF
    else:
        errors.append(
            f"syntax error on line {token.line_num}. second operand, {op2.value}, to add instruction must be a register, literal value, or a dereference."
        )
        return None

    return Node(opcode=Opcode.ADD, address_mode=mode, op1=op1.value, op2=op2.value)


def and_token(token, iter):
    try:
        op1 = next(iter)
        op2 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. and instruction requires two operands."
        )
        return None

    # first operand must be a register
    if op1.type != Type.REGISTER:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to and instruction must be a register."
        )
        return None
    if op2.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op2.type == Type.LITERAL and isinstance(op2.value, int):
        mode = AddressMode.LITERAL
    elif op2.type == Type.DEREF and isinstance(op2.value, int):
        mode = AddressMode.MEMORY
    elif op2.type == Type.DEREF:
        mode = AddressMode.REGISTERDEREF
    else:
        errors.append(
            f"syntax error on line {token.line_num}. second operand, {op2.value}, to and instruction must be a register, literal value, or a dereference."
        )
        return None

    return Node(opcode=Opcode.AND, address_mode=mode, op1=op1.value, op2=op2.value)


def call_token(token, iter):
    try:
        op1 = next(iter)
        op2 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. call instruction requires two operands."
        )
        return None

    # first operand must be a register
    if op1.type != Type.REGISTER:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to call instruction must be a register."
        )
        return None
    if op2.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op2.type == Type.LITERAL and isinstance(op2.value, int):
        mode = AddressMode.LITERAL
    elif op2.type == Type.DEREF and isinstance(op2.value, int):
        mode = AddressMode.MEMORY
    elif op2.type == Type.DEREF:
        mode = AddressMode.REGISTERDEREF
    else:
        errors.append(
            f"syntax error on line {token.line_num}. second operand, {op2.value}, to call instruction must be a register, literal value, or a dereference."
        )
        return None

    return Node(opcode=Opcode.CALL, address_mode=mode, op1=op1.value, op2=op2.value)


def compare_token(token, iter):
    try:
        op1 = next(iter)
        op2 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. compare instruction requires two operands."
        )
        return None

    # first operand must be a register
    if op1.type != Type.REGISTER:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to compare instruction must be a register."
        )
        return None
    if op2.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op2.type == Type.LITERAL and isinstance(op2.value, int):
        mode = AddressMode.LITERAL
    elif op2.type == Type.DEREF and isinstance(op2.value, int):
        mode = AddressMode.MEMORY
    elif op2.type == Type.DEREF:
        mode = AddressMode.REGISTERDEREF
    else:
        errors.append(
            f"syntax error on line {token.line_num}. second operand, {op2.value}, to compare instruction must be a register, literal value, or a dereference."
        )
        return None

    return Node(opcode=Opcode.COMPARE, address_mode=mode, op1=op1.value, op2=op2.value)


def divide_token(token, iter):
    try:
        op1 = next(iter)
        op2 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. divide instruction requires two operands."
        )
        return None

    # first operand must be a register
    if op1.type != Type.REGISTER:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to divide instruction must be a register."
        )
        return None
    if op2.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op2.type == Type.LITERAL and isinstance(op2.value, int):
        mode = AddressMode.LITERAL
    elif op2.type == Type.DEREF and isinstance(op2.value, int):
        mode = AddressMode.MEMORY
    elif op2.type == Type.DEREF:
        mode = AddressMode.REGISTERDEREF
    else:
        errors.append(
            f"syntax error on line {token.line_num}. second operand, {op2.value}, to divide instruction must be a register, literal value, or a dereference."
        )
        return None

    return Node(opcode=Opcode.DIVIDE, address_mode=mode, op1=op1.value, op2=op2.value)


def halt_token(token, iter):
    return Node(opcode=Opcode.HALT, address_mode=AddressMode.NONE, op1=None, op2=None)


def input_token(token, iter):
    try:
        op = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. input instruction requires an operand."
        )
        return None

    if op.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op.type == Type.LITERAL and isinstance(op.value, int):
        mode = AddressMode.LITERAL
    elif op.type == Type.DEREF and isinstance(op.value, int):
        mode = AddressMode.MEMORY
    elif op.type == Type.DEREF:
        mode = AddressMode.REGISTERDEREF
    else:
        errors.append(
            f"syntax error on line {token.line_num}. the operand, {op.value}, to input instruction must be a register, literal value, or a dereference."
        )
        return None

    return Node(opcode=Opcode.INPUT, address_mode=mode, op1=None, op2=op.value)


def jump_token(token, iter):
    try:
        op1 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. jump instruction requires an operand."
        )
        return None
    resolve_symbol = False
    val = op1.value
    if op1.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op1.type == Type.LITERAL:
        mode = AddressMode.LITERAL
        if isinstance(op1.value, str):  # type(0) != type(op1.value):
            if op1.value in symbol_table:
                val = symbol_table[op1.value]
            else:
                resolve_symbol = True
    else:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to jump instruction must be a register, literal value, or a label name."
        )
        return None
    return Node(
        opcode=Opcode.JUMP,
        address_mode=mode,
        op1=None,
        op2=val,
        resolve_symbol=resolve_symbol,
    )


def jumpeq_token(token, iter):
    try:
        op1 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. jumpeq instruction requires an operand."
        )
        return None
    resolve_symbol = False
    val = op1.value
    if op1.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op1.type == Type.LITERAL:
        mode = AddressMode.LITERAL
        if isinstance(op1.value, str):  # type(0) != type(op1.value):
            if op1.value in symbol_table:
                val = symbol_table[op1.value]
            else:
                resolve_symbol = True
    else:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to jumpeq instruction must be a register, literal value, or a label name."
        )
        return None
    return Node(
        opcode=Opcode.JUMPEQ,
        address_mode=mode,
        op1=None,
        op2=val,
        resolve_symbol=resolve_symbol,
    )


def jumpgreater_token(token, iter):
    try:
        op1 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. jumpgreater instruction requires an operand."
        )
        return None
    resolve_symbol = False
    val = op1.value
    if op1.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op1.type == Type.LITERAL:
        mode = AddressMode.LITERAL
        if isinstance(op1.value, str):  # type(0) != type(op1.value):
            if op1.value in symbol_table:
                val = symbol_table[op1.value]
            else:
                resolve_symbol = True
    else:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to jumpgreater instruction must be a register, literal value, or a label name."
        )
        return None
    return Node(
        opcode=Opcode.JUMPGREATER,
        address_mode=mode,
        op1=None,
        op2=val,
        resolve_symbol=resolve_symbol,
    )


def jumpgreatereq_token(token, iter):
    try:
        op1 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. jumpgreatereq instruction requires an operand."
        )
        return None
    resolve_symbol = False
    val = op1.value
    if op1.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op1.type == Type.LITERAL:
        mode = AddressMode.LITERAL
        if isinstance(op1.value, str):  # type(0) != type(op1.value):
            if op1.value in symbol_table:
                val = symbol_table[op1.value]
            else:
                resolve_symbol = True
    else:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to jumpgreatereq instruction must be a register, literal value, or a label name."
        )
        return None
    return Node(
        opcode=Opcode.JUMPGREATEREQ,
        address_mode=mode,
        op1=None,
        op2=val,
        resolve_symbol=resolve_symbol,
    )


def jumpless_token(token, iter):
    try:
        op1 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. jumpless instruction requires an operand."
        )
        return None
    resolve_symbol = False
    val = op1.value
    if op1.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op1.type == Type.LITERAL:
        mode = AddressMode.LITERAL
        if isinstance(op1.value, str):  # type(0) != type(op1.value):
            if op1.value in symbol_table:
                val = symbol_table[op1.value]
            else:
                resolve_symbol = True
    else:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to jumpless instruction must be a register, literal value, or a label name."
        )
        return None
    return Node(
        opcode=Opcode.JUMPLESS,
        address_mode=mode,
        op1=None,
        op2=val,
        resolve_symbol=resolve_symbol,
    )


def jumplesseq_token(token, iter):
    try:
        op1 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. jumplesseq instruction requires an operand."
        )
        return None
    resolve_symbol = False
    val = op1.value
    if op1.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op1.type == Type.LITERAL:
        mode = AddressMode.LITERAL
        if isinstance(op1.value, str):  # type(0) != type(op1.value):
            if op1.value in symbol_table:
                val = symbol_table[op1.value]
            else:
                resolve_symbol = True
    else:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to jumplesseq instruction must be a register, literal value, or a label name."
        )
        return None
    return Node(
        opcode=Opcode.JUMPLESSEQ,
        address_mode=mode,
        op1=None,
        op2=val,
        resolve_symbol=resolve_symbol,
    )


def jumpnoteq_token(token, iter):
    try:
        op1 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. jumpnoteq instruction requires an operand."
        )
        return None
    resolve_symbol = False
    val = op1.value
    if op1.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op1.type == Type.LITERAL:
        mode = AddressMode.LITERAL
        if isinstance(op1.value, str):  # type(0) != type(op1.value):
            if op1.value in symbol_table:
                val = symbol_table[op1.value]
            else:
                resolve_symbol = True
    else:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to jumpnoteq instruction must be a register, literal value, or a label name."
        )
        return None
    return Node(
        opcode=Opcode.JUMPNOTEQ,
        address_mode=mode,
        op1=None,
        op2=val,
        resolve_symbol=resolve_symbol,
    )


def load_token(token, iter):
    try:
        op1 = next(iter)
        op2 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. load instruction requires two operands."
        )
        return None
    resolve_symbol = False

    # first operand must be a register
    if op1.type != Type.REGISTER:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to load instruction must be a register."
        )
        return None
    if op2.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op2.type == Type.LITERAL and isinstance(op2.value, int):
        mode = AddressMode.LITERAL
    elif op2.type == Type.DEREF and isinstance(op2.value, int):
        mode = AddressMode.MEMORY
    elif op2.type == Type.DEREF:
        mode = AddressMode.REGISTERDEREF
    else:
        mode = AddressMode.LITERAL
        resolve_symbol = True

    return Node(
        opcode=Opcode.LOAD,
        address_mode=mode,
        op1=op1.value,
        op2=op2.value,
        resolve_symbol=resolve_symbol,
    )


def loadbyte_token(token, iter):
    try:
        op1 = next(iter)
        op2 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. loadbyte instruction requires two operands."
        )
        return None
    resolve_symbol = False

    # first operand must be a register
    if op1.type != Type.REGISTER:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to loadbyte instruction must be a register."
        )
        return None
    if op2.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op2.type == Type.LITERAL and isinstance(op2.value, int):
        mode = AddressMode.LITERAL
    elif op2.type == Type.DEREF and isinstance(op2.value, int):
        mode = AddressMode.MEMORY
    elif op2.type == Type.DEREF:
        mode = AddressMode.REGISTERDEREF
    else:
        mode = AddressMode.LITERAL
        resolve_symbol = True

    return Node(
        opcode=Opcode.LOADBYTE,
        address_mode=mode,
        op1=op1.value,
        op2=op2.value,
        resolve_symbol=resolve_symbol,
    )


def modulus_token(token, iter):
    try:
        op1 = next(iter)
        op2 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. modulus instruction requires two operands."
        )
        return None

    # first operand must be a register
    if op1.type != Type.REGISTER:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to modulus instruction must be a register."
        )
        return None
    if op2.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op2.type == Type.LITERAL and isinstance(op2.value, int):
        mode = AddressMode.LITERAL
    elif op2.type == Type.DEREF and isinstance(op2.value, int):
        mode = AddressMode.MEMORY
    elif op2.type == Type.DEREF:
        mode = AddressMode.REGISTERDEREF
    else:
        errors.append(
            f"syntax error on line {token.line_num}. second operand, {op2.value}, to modulus instruction must be a register, literal value, or a dereference."
        )
        return None

    return Node(opcode=Opcode.MODULUS, address_mode=mode, op1=op1.value, op2=op2.value)


def multiply_token(token, iter):
    try:
        op1 = next(iter)
        op2 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. multiply instruction requires two operands."
        )
        return None

    # first operand must be a register
    if op1.type != Type.REGISTER:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to multiply instruction must be a register."
        )
        return None
    if op2.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op2.type == Type.LITERAL and isinstance(op2.value, int):
        mode = AddressMode.LITERAL
    elif op2.type == Type.DEREF and isinstance(op2.value, int):
        mode = AddressMode.MEMORY
    elif op2.type == Type.DEREF:
        mode = AddressMode.REGISTERDEREF
    else:
        errors.append(
            f"syntax error on line {token.line_num}. second operand, {op2.value}, to multiply instruction must be a register, literal value, or a dereference."
        )
        return None

    return Node(opcode=Opcode.MULTIPLY, address_mode=mode, op1=op1.value, op2=op2.value)


def nop_token(token, iter):
    return Node(opcode=Opcode.NOP, address_mode=AddressMode.NONE, op1=None, op2=None)


def not_token(token, iter):
    try:
        op = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. not instruction requires an operand."
        )
        return None

    if op.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op.type == Type.LITERAL and isinstance(op.value, int):
        mode = AddressMode.LITERAL
    elif op.type == Type.DEREF and isinstance(op.value, int):
        mode = AddressMode.MEMORY
    elif op.type == Type.DEREF:
        mode = AddressMode.REGISTERDEREF
    else:
        errors.append(
            f"syntax error on line {token.line_num}. second operand, {op.value}, to not instruction must be a register, literal value, or a dereference."
        )
        return None

    return Node(opcode=Opcode.NOT, address_mode=mode, op1=None, op2=op.value)


def or_token(token, iter):
    try:
        op1 = next(iter)
        op2 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. or instruction requires two operands."
        )
        return None

    # first operand must be a register
    if op1.type != Type.REGISTER:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to or instruction must be a register."
        )
        return None
    if op2.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op2.type == Type.LITERAL and isinstance(op2.value, int):
        mode = AddressMode.LITERAL
    elif op2.type == Type.DEREF and isinstance(op2.value, int):
        mode = AddressMode.MEMORY
    elif op2.type == Type.DEREF:
        mode = AddressMode.REGISTERDEREF
    else:
        errors.append(
            f"syntax error on line {token.line_num}. second operand, {op2.value}, to or instruction must be a register, literal value, or a dereference."
        )
        return None

    return Node(opcode=Opcode.OR, address_mode=mode, op1=op1.value, op2=op2.value)


def output_token(token, iter):
    try:
        op = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. output instruction requires an operand."
        )
        return None

    if op.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op.type == Type.LITERAL and isinstance(op.value, int):
        mode = AddressMode.LITERAL
    elif op.type == Type.DEREF and isinstance(op.value, int):
        mode = AddressMode.MEMORY
    elif op.type == Type.DEREF:
        mode = AddressMode.REGISTERDEREF
    else:
        errors.append(
            f"syntax error on line {token.line_num}. the operand, {op.value}, to output instruction must be a register, literal value, or a dereference."
        )
        return None

    return Node(opcode=Opcode.OUTPUT, address_mode=mode, op1=None, op2=op.value)


def pop_token(token, iter):
    try:
        op1 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. pop instruction requires an operand."
        )
        return None
    resolve_symbol = False
    val = op1.value
    if op1.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op1.type == Type.LITERAL:
        mode = AddressMode.LITERAL
        if isinstance(op1.value, str):  # type(0) != type(op1.value):
            if op1.value in symbol_table:
                val = symbol_table[op1.value]
            else:
                resolve_symbol = True
    else:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to pop instruction must be a register, literal value, or a label name."
        )
        return None
    return Node(
        opcode=Opcode.POP,
        address_mode=mode,
        op1=None,
        op2=val,
        resolve_symbol=resolve_symbol,
    )


def popbyte_token(token, iter):
    try:
        op1 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. popbyte instruction requires an operand."
        )
        return None
    resolve_symbol = False
    val = op1.value
    if op1.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op1.type == Type.LITERAL:
        mode = AddressMode.LITERAL
        if isinstance(op1.value, str):
            if op1.value in symbol_table:
                val = symbol_table[op1.value]
            else:
                resolve_symbol = True
    else:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to popbyte instruction must be a register, literal value, or a label name."
        )
        return None
    return Node(
        opcode=Opcode.POPBYTE,
        address_mode=mode,
        op1=None,
        op2=val,
        resolve_symbol=resolve_symbol,
    )


def push_token(token, iter):
    try:
        op1 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. push instruction requires an operand."
        )
        return None
    resolve_symbol = False
    val = op1.value
    if op1.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op1.type == Type.LITERAL:
        mode = AddressMode.LITERAL
        if isinstance(op1.value, str):
            if op1.value in symbol_table:
                val = symbol_table[op1.value]
            else:
                resolve_symbol = True
    else:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to push instruction must be a register, literal value, or a label name."
        )
        return None
    return Node(
        opcode=Opcode.PUSH,
        address_mode=mode,
        op1=None,
        op2=val,
        resolve_symbol=resolve_symbol,
    )


def pushbyte_token(token, iter):
    try:
        op1 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. pushbyte instruction requires an operand."
        )
        return None
    resolve_symbol = False
    val = op1.value
    if op1.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op1.type == Type.LITERAL:
        mode = AddressMode.LITERAL
        if isinstance(op1.value, str):  # type(0) != type(op1.value):
            if op1.value in symbol_table:
                val = symbol_table[op1.value]
            else:
                resolve_symbol = True
    else:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to pushbyte instruction must be a register, literal value, or a label name."
        )
        return None
    return Node(
        opcode=Opcode.PUSHBYTE,
        address_mode=mode,
        op1=None,
        op2=val,
        resolve_symbol=resolve_symbol,
    )


def return_token(token, iter):
    return Node(opcode=Opcode.RETURN, address_mode=AddressMode.NONE, op1=None, op2=None)


def store_token(token, iter):
    try:
        op1 = next(iter)
        op2 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. store instruction requires two operands."
        )
        return None

    # first operand must be a register
    if op1.type != Type.REGISTER:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to store instruction must be a register."
        )
        return None
    if op2.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op2.type == Type.LITERAL and isinstance(op2.value, int):
        mode = AddressMode.LITERAL
    elif op2.type == Type.DEREF and isinstance(op2.value, int):
        mode = AddressMode.MEMORY
    elif op2.type == Type.DEREF:
        mode = AddressMode.REGISTERDEREF
    else:
        errors.append(
            f"syntax error on line {token.line_num}. second operand, {op2.value}, to store instruction must be a register, literal value, or a dereference."
        )
        return None

    return Node(opcode=Opcode.STORE, address_mode=mode, op1=op1.value, op2=op2.value)


def storebyte_token(token, iter):
    try:
        op1 = next(iter)
        op2 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. storebyte instruction requires two operands."
        )
        return None

    # first operand must be a register
    if op1.type != Type.REGISTER:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to storebyte instruction must be a register."
        )
        return None
    if op2.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op2.type == Type.LITERAL and isinstance(op2.value, int):
        mode = AddressMode.LITERAL
    elif op2.type == Type.DEREF and isinstance(op2.value, int):
        mode = AddressMode.MEMORY
    elif op2.type == Type.DEREF:
        mode = AddressMode.REGISTERDEREF
    else:
        errors.append(
            f"syntax error on line {token.line_num}. second operand, {op2.value}, to storebyte instruction must be a register, literal value, or a dereference."
        )
        return None

    return Node(
        opcode=Opcode.STOREBYTE, address_mode=mode, op1=op1.value, op2=op2.value
    )


def subtract_token(token, iter):
    try:
        op1 = next(iter)
        op2 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. subtract instruction requires two operands."
        )
        return None

    # first operand must be a register
    if op1.type != Type.REGISTER:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to subtract instruction must be a register."
        )
        return None
    if op2.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op2.type == Type.LITERAL and isinstance(op2.value, int):
        mode = AddressMode.LITERAL
    elif op2.type == Type.DEREF and isinstance(op2.value, int):
        mode = AddressMode.MEMORY
    elif op2.type == Type.DEREF:
        mode = AddressMode.REGISTERDEREF
    else:
        errors.append(
            f"syntax error on line {token.line_num}. second operand, {op2.value}, to subtract instruction must be a register, literal value, or a dereference."
        )
        return None

    return Node(opcode=Opcode.SUBTRACT, address_mode=mode, op1=op1.value, op2=op2.value)


def syscall_token(token, iter):
    return Node(
        opcode=Opcode.SYSCALL, address_mode=AddressMode.NONE, op1=None, op2=None
    )


def xor_token(token, iter):
    try:
        op1 = next(iter)
        op2 = next(iter)
    except StopIteration:
        errors.append(
            f"unexpected end of file on line {token.line_num}. xor instruction requires two operands."
        )
        return None

    # first operand must be a register
    if op1.type != Type.REGISTER:
        errors.append(
            f"syntax error on line {token.line_num}. first operand to xor instruction must be a register."
        )
        return None
    if op2.type == Type.REGISTER:
        mode = AddressMode.REGISTER
    elif op2.type == Type.LITERAL and isinstance(op2.value, int):
        mode = AddressMode.LITERAL
    elif op2.type == Type.DEREF and isinstance(op2.value, int):
        mode = AddressMode.MEMORY
    elif op2.type == Type.DEREF:
        mode = AddressMode.REGISTERDEREF
    else:
        errors.append(
            f"syntax error on line {token.line_num}. second operand, {op2.value}, to xor instruction must be a register, literal value, or a dereference."
        )
        return None

    return Node(opcode=Opcode.XOR, address_mode=mode, op1=op1.value, op2=op2.value)


def deref_token(token, iter):
    errors.append(f"syntax error on line {token.line_num}. missing an instruction?")
    return None


def literal_token(token, iter):
    errors.append(f"syntax error on line {token.line_num}. missing an instruction?")
    return None


def register_token(token, iter):
    errors.append(f"syntax error on line {token.line_num}. missing an instruction?")
    return None


def parse(tokens):
    nodes = []
    toks = iter(tokens)
    while True:
        token = next(toks, "end")
        if token == "end":
            break
        elif token.type == Type.ADD:
            node = add_token(token, toks)
        elif token.type == Type.AND:
            node = and_token(token, toks)
        elif token.type == Type.CALL:
            node = call_token(token, toks)
        elif token.type == Type.COMPARE:
            node = compare_token(token, toks)
        elif token.type == Type.DIVIDE:
            node = divide_token(token, toks)
        elif token.type == Type.HALT:
            node = halt_token(token, toks)
        elif token.type == Type.INPUT:
            node = input_token(token, toks)
        elif token.type == Type.JUMP:
            node = jump_token(token, toks)
        elif token.type == Type.JUMPEQ:
            node = jumpeq_token(token, toks)
        elif token.type == Type.JUMPGREATER:
            node = jumpgreater_token(token, toks)
        elif token.type == Type.JUMPLESS:
            node = jumpless_token(token, toks)
        elif token.type == Type.JUMPLESSEQ:
            node = jumplesseq_token(token, toks)
        elif token.type == Type.JUMPNOTEQ:
            node = jumpnoteq_token(token, toks)
        elif token.type == Type.LOAD:
            node = load_token(token, toks)
        elif token.type == Type.LOADBYTE:
            node = loadbyte_token(token, toks)
        elif token.type == Type.MODULUS:
            node = modulus_token(token, toks)
        elif token.type == Type.MULTIPLY:
            node = multiply_token(token, toks)
        elif token.type == Type.NOP:
            node = nop_token(token, toks)
        elif token.type == Type.NOT:
            node = not_token(token, toks)
        elif token.type == Type.OR:
            node = or_token(token, toks)
        elif token.type == Type.OUTPUT:
            node = output_token(token, toks)
        elif token.type == Type.POP:
            node = pop_token(token, toks)
        elif token.type == Type.POPBYTE:
            node = popbyte_token(token, toks)
        elif token.type == Type.PUSH:
            node = push_token(token, toks)
        elif token.type == Type.PUSHBYTE:
            node = pushbyte_token(token, toks)
        elif token.type == Type.RETURN:
            node = return_token(token, toks)
        elif token.type == Type.STORE:
            node = store_token(token, toks)
        elif token.type == Type.STOREBYTE:
            node = storebyte_token(token, toks)
        elif token.type == Type.SUBTRACT:
            node = subtract_token(token, toks)
        elif token.type == Type.SYSCALL:
            node = syscall_token(token, toks)
        elif token.type == Type.XOR:
            node = xor_token(token, toks)

        elif token.type == Type.DEREF:
            node = deref_token(token, toks)
        elif token.type == Type.LABEL:
            # each node will be 8 bytes, plus the 8 byte header
            symbol_table[token.value] = len(nodes) * 8 + 8
            continue
        elif token.type == Type.LITERAL:
            node = literal_token(token, toks)
        elif token.type == Type.REGISTER:
            node = register_token(token, toks)
        elif token.type == Type.VARIABLE:
            lit = next(toks)
            symbol_table[token.value] = lit.value
            continue
        else:
            print(f"unrecognized token? why did this happen. {token}")
            continue

        nodes.append(node)

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    program_length = len(nodes) * 8 + 8
    data = []

    # resolve symbols
    for node in nodes:
        if node.resolve_symbol and type(0) != type(symbol_table[node.op2]):
            data.append(symbol_table[node.op2])
            l = program_length
            program_length += len(symbol_table[node.op2])
            node.op2 = l
        elif node.resolve_symbol:
            node.op2 = symbol_table[node.op2]

    nodes.extend(data)
    return nodes
