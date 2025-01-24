from __future__ import annotations
from dataclasses import dataclass
from typing import NamedTuple
from enum import Enum
import sys
import re

REGEX_REGISTER = r"Register \w: (\d+)"
REGEX_INSTRUCTIONS = r"Program: ((\d+,?)+)"


def read_input() -> Computer:
    with open(sys.argv[1]) as f:
        registers = []
        while line := f.readline().strip():
            registers.append(int(re.match(REGEX_REGISTER, line).group(1)))
        line = f.readline().strip()
        instructions = list(
            map(int, re.match(REGEX_INSTRUCTIONS, line).group(1).split(","))
        )
        computer = Computer(
            register_a=registers[0],
            register_b=registers[1],
            register_c=registers[2],
            operations=instructions[::2],
            operands=instructions[1::2],
        )
    return computer


@dataclass
class Computer:

    register_a: int
    register_b: int
    register_c: int

    operations: list[int]  # maybe list callable
    operands: list[int]
    instruction_pointer: int = 0
    stopped: bool = False

    def next(self):
        if not self.stopped:
            self.instruction_pointer += 1
        else:
            self.stopped = False
        return self.instruction_pointer

    def adv(self, operand: int):
        self.register_a = int(self.register_a / 2 ** self.combo_map(operand))

    def bxl(self, operand: int):
        self.register_b = self.register_b ^ operand

    def bst(self, operand: int):
        self.register_b = self.combo_map(operand) % 8

    def jnz(self, operand: int):
        if self.register_a == 0:
            return
        else:
            self.instruction_pointer = operand // 2
            self.stopped = True

    def bxc(self, operand: int):
        self.register_b = self.register_b ^ self.register_c

    def out(self, operand: int):
        return self.combo_map(operand) % 8

    def bdv(self, operand: int):
        self.register_b = int(self.register_a / 2 ** self.combo_map(operand))

    def cdv(self, operand: int):
        self.register_c = int(self.register_a / 2 ** self.combo_map(operand))

    def combo_map(self, combo_operand: int) -> int:
        match (combo_operand):
            case combo_operand if combo_operand in [0, 1, 2, 3]:
                return combo_operand
            case 4:
                return self.register_a
            case 5:
                return self.register_b
            case 6:
                return self.register_c
            case 7:
                raise Exception(
                    "7 is reserved and not supposed to appear in valid programs"
                )
            case _:
                exc = "Unrecognized symbol {}".format(combo_operand)
                raise Exception(exc)

    def operation_map(self, op_code: int) -> callable:
        match (op_code):
            case 0:
                return self.adv
            case 1:
                return self.bxl
            case 2:
                return self.bst
            case 3:
                return self.jnz
            case 4:
                return self.bxc
            case 5:
                return self.out
            case 6:
                return self.bdv
            case 7:
                return self.cdv
            case _:
                return self.adv


if __name__ == "__main__":
    computer = read_input()
    output = []
    while computer.instruction_pointer < len(computer.operations):
        i = computer.instruction_pointer

        res = computer.operation_map(computer.operations[i])(computer.operands[i])
        if computer.operations[i] == 5:
            output.append(res)
        computer.next()

    print(",".join([str(o) for o in output if o != None]))
