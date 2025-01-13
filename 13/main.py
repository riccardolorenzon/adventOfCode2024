from typing import NamedTuple, List
import re
import sys
from functools import lru_cache


# Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400
BUTTON = re.compile(r"Button \w: X\+(\d+), Y\+(\d+)")
PRIZE = re.compile(r"Prize: X=(\d+), Y=(\d+)")

BUTTON_A_TOKENS = 3
BUTTON_B_TOKENS = 1


class Button(NamedTuple):
    tokens: int
    x: int
    y: int


class Machine(NamedTuple):
    id: int
    button_a: Button
    button_b: Button
    prize_x: int
    prize_y: int


cache = {}


def get_number_of_tokens(machine: Machine):
    a, b = machine.button_a, machine.button_b
    mul_b = (a.y * machine.prize_x - machine.prize_y * a.x) / (a.y * b.x - b.y * a.x)
    if mul_b != int(mul_b):
        return 0
    mul_b = int(mul_b)

    mul_a = (machine.prize_x - (mul_b * b.x)) / a.x
    if mul_a != int(mul_a):
        return 0
    mul_a = int(mul_a)
    return BUTTON_A_TOKENS * mul_a + BUTTON_B_TOKENS * int(mul_b)


def correct_machines(machines: List[Machine]) -> List[Machine]:
    return [
        Machine(
            id=m.id,
            button_a=m.button_a,
            button_b=m.button_b,
            prize_x=10000000000000 + m.prize_x,
            prize_y=10000000000000 + m.prize_y,
        )
        for m in machines
    ]


def read_input() -> List[Machine]:
    with open(sys.argv[1]) as f:
        lines = [l.strip() for l in f.read().splitlines() if l]
    i = 0
    machines = []
    while i < len(lines):
        button_a = Button(
            tokens=BUTTON_A_TOKENS,
            x=int(BUTTON.match(lines[i])[1]),
            y=int(BUTTON.match(lines[i])[2]),
        )
        i += 1
        button_b = Button(
            tokens=BUTTON_B_TOKENS,
            x=int(BUTTON.match(lines[i])[1]),
            y=int(BUTTON.match(lines[i])[2]),
        )
        i += 1
        machine = Machine(
            id=i,
            button_a=button_a,
            button_b=button_b,
            prize_x=int(PRIZE.match(lines[i])[1]),
            prize_y=int(PRIZE.match(lines[i])[2]),
        )
        machines.append(machine)
        i += 1
    return machines


if __name__ == "__main__":
    machines = read_input()
    total = 0
    for machine in machines:
        total += get_number_of_tokens(machine)
    print(total)
    total = 0
    for machine in correct_machines(machines):
        total += get_number_of_tokens(machine)
    print(total)
