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


def get_number_of_tokens(machine: Machine, prize_x, prize_y):
    if f"{machine.id}_{prize_x}_{prize_y}" in cache:
        return cache[f"{machine.id}_{prize_x}_{prize_y}"]
    if prize_x < 0 or prize_y < 0:
        return float("inf")
    elif prize_x == 0 and prize_y == 0:
        return 0
    else:
        cache[f"{machine.id}_{prize_x}_{prize_y}"] = min(
            machine.button_a.tokens
            + get_number_of_tokens(
                machine, prize_x - machine.button_a.x, prize_y - machine.button_a.y
            ),
            machine.button_b.tokens
            + get_number_of_tokens(
                machine, prize_x - machine.button_b.x, prize_y - machine.button_b.y
            ),
        )
        return cache[f"{machine.id}_{prize_x}_{prize_y}"]


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
        res = get_number_of_tokens(machine, machine.prize_x, machine.prize_y)
        if res != float("inf"):
            total += res
    print(total)
