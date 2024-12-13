from collections import defaultdict
from io import TextIOWrapper
import sys
from typing import List


def check_update_order(cannot_be_before, update):
    for i, element in enumerate(update):
        wrong_position_elements = set(update[:i]).intersection(
            cannot_be_before[element]
        )
        if len(wrong_position_elements) != 0:
            return False
    return True


def part_1(cannot_be_before, updates):
    total_middle_elements = 0
    for update in updates:
        check = check_update_order(cannot_be_before, update)
        if check:
            total_middle_elements += int(update[len(update) // 2])
    print(total_middle_elements)


def part_2(cannot_be_before, updates: List[List[str]]):
    total_middle_elements = 0
    for update in updates:
        is_fixed = False
        i = 0
        while i < len(update):
            page = update[i]
            j = 0
            sh_el = []
            while j < i:
                if update[j] in cannot_be_before[page]:
                    is_fixed = True
                    sh_el.append(update.pop(j))
                    i -= 1
                else:
                    j += 1
            update[i + 1 : i + 1] = sh_el
            i += 1

        if is_fixed:
            total_middle_elements += int(update[len(update) // 2])
            is_fixed = False

    print(total_middle_elements)


def process_input(f: TextIOWrapper):
    cannot_be_before = defaultdict(set)
    while line := f.readline():
        line = line.rstrip()
        if line == "":
            break
        val1, val2 = line.split("|")
        cannot_be_before[val1].add(val2)
    updates = [line.split(",") for line in f.read().splitlines()]
    return cannot_be_before, updates


if __name__ == "__main__":
    input_file = sys.argv[1]
    with open(input_file) as f:
        cannot_be_before, updates = process_input(f)
    part_1(cannot_be_before, updates)
    part_2(cannot_be_before, updates)
