from collections import defaultdict
from io import TextIOWrapper
import sys


def check_update_order(ordering, update):
    for i, element in enumerate(update):
        if len(set(update[:i]).intersection(ordering[element])) != 0:
            return False
    return True


def part_1(ordering, updates):
    total_middle_elements = 0
    for update in updates:
        if check_update_order(ordering, update):
            total_middle_elements += int(update[len(update) // 2])
    print(total_middle_elements)


def part_2(): ...


def process_input(f: TextIOWrapper):
    ordering = defaultdict(set)
    while line := f.readline():
        line = line.rstrip()
        if line == "":
            break
        val1, val2 = line.split("|")
        ordering[val1].add(val2)
    updates = [line.split(",") for line in f.read().splitlines()]
    return ordering, updates


if __name__ == "__main__":
    input_file = sys.argv[1]
    with open(input_file) as f:
        ordering, updates = process_input(f)

    part_1(ordering, updates)
