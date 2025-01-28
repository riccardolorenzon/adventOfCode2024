import sys
from functools import cache


def read_input() -> tuple[list[str], list[str]]:
    with open(sys.argv[1]) as f:
        towels = list(map(lambda x: x.strip(), f.readline().strip().split(",")))
        f.readline()
        combinations = []
        while line := f.readline():
            combinations.append(line.strip())
    return (towels, combinations)


@cache
def check_combination(pattern: str, towels: tuple[str]) -> bool:
    if pattern == "":
        return True
    for towel in towels:
        if pattern[: len(towel)] == towel:
            if check_combination(pattern[len(towel) :], towels):
                return True
    return False


if __name__ == "__main__":
    towels, combinations = read_input()
    possible_combinations = 0
    for c in combinations:
        if check_combination(c, tuple(towels)):
            possible_combinations += 1
    print(f"Number of possible design patterns -> {possible_combinations}")
