from collections import defaultdict, namedtuple
from functools import lru_cache
from typing import List, Tuple
import sys

BLINKS = 75

Stone = namedtuple("Stone", ["digits", "qty"])


def read_input() -> List[Stone]:
    stones = []
    with open(sys.argv[1]) as f:
        digits = f.readline().rstrip().split(" ")
        for digit in digits:
            stones.append(Stone(digits=int(digit), qty=1))
    return stones


def post_blink_stone(stone: Stone) -> List[Stone]:
    if stone.digits == 0:
        return [Stone(digits=1, qty=stone.qty)]
    elif (digits := len(stone_str := str(stone.digits))) % 2 == 0:
        return [
            Stone(int(stone_str[: digits // 2]), stone.qty),
            Stone(int(stone_str[digits // 2 :]), stone.qty),
        ]
    return [Stone(2024 * stone.digits, stone.qty)]


def compact(stones: Tuple[Stone]) -> Tuple[int]:
    new_stones = defaultdict(lambda: 0)
    for stone in stones:
        new_stones[stone.digits] += stone.qty
    return [Stone(k, v) for (k, v) in new_stones.items()]


@lru_cache
def blink_flow(stones: Tuple[Stone], blinks: int) -> int:
    if blinks == 0:
        return sum([stone.qty for stone in stones])
    new_stones = []
    for stone in stones:
        new_stones.extend(post_blink_stone(stone))
    stones = compact(new_stones)
    return blink_flow(tuple(stones), blinks - 1)


if __name__ == "__main__":
    stones = read_input()
    print(f"Number of stones {blink_flow(tuple(stones), BLINKS) }")
