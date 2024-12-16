from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
import sys
from typing import List


class Direction(Enum):
    NORTH = "^"
    SOUTH = "v"
    EST = ">"
    WEST = "<"


@dataclass
class Block:
    i: int = None
    j: int = None


@dataclass
class VisitedCell:
    guard_directions: List[Direction]

    def __repr__(self):
        if self.guard_directions:
            return "".join(
                [direction.value for direction in self.guard_directions]
            ).ljust(4, "*")
        else:
            return "."


@dataclass
class Guard:
    i: int
    j: int
    direction: Direction
    max_row: int
    max_column: int

    def next(self):
        match (self.direction):
            case Direction.NORTH:
                self.i -= 1
            case Direction.SOUTH:
                self.i += 1
            case Direction.EST:
                self.j += 1
            case Direction.WEST:
                self.j -= 1
        if (
            self.i < 0
            or self.j < 0
            or self.i >= self.max_row
            or self.j >= self.max_column
        ):
            raise StopIteration

    def previous(self):
        match (self.direction):
            case Direction.NORTH:
                self.i += 1
            case Direction.SOUTH:
                self.i -= 1
            case Direction.EST:
                self.j -= 1
            case Direction.WEST:
                self.j += 1

    def turn(self):
        match (self.direction):
            case Direction.NORTH:
                self.direction = Direction.EST
            case Direction.SOUTH:
                self.direction = Direction.WEST
            case Direction.EST:
                self.direction = Direction.SOUTH
            case Direction.WEST:
                self.direction = Direction.NORTH


class InfiniteLoop(BaseException):
    pass


def part_2(lab_map: List[List[str]], guard: Guard) -> int:
    blocks = 0
    for x, line in enumerate(lab_map):
        for y, cell in enumerate(line):
            original_map = deepcopy(lab_map)
            original_guard = deepcopy(guard)
            if cell == "X":
                original_map[x][y] = "O"
                try:
                    part_1(original_map, original_guard)
                except InfiniteLoop as e:
                    blocks += 1
    print(f"The total number of way to block the guard is {blocks}")
    return blocks


def part_1(lab_map: List[List[str]], guard: Guard) -> int:
    steps = 0
    visited_spots = [
        [None for _ in range(len(lab_map[0]))] for _ in range(len(lab_map))
    ]
    try:
        while True:
            if visited_spots[guard.i][guard.j] is None:
                visited_spots[guard.i][guard.j] = VisitedCell([guard.direction])
            else:
                if guard.direction in visited_spots[guard.i][guard.j].guard_directions:
                    raise InfiniteLoop
                else:
                    visited_spots[guard.i][guard.j].guard_directions.append(
                        guard.direction
                    )
            if lab_map[guard.i][guard.j] in ["#", "O"]:
                guard.previous()
                guard.turn()
            else:
                if lab_map[guard.i][guard.j] != "X":
                    steps += 1
                lab_map[guard.i][guard.j] = "X"
            guard.next()

    except StopIteration as e:
        pass
    return steps


def read_input(filename: str):
    matrix = []
    with open(filename) as f:
        r = 0
        g = Guard(0, 0, None, None, None)
        while line := f.readline():
            for data in Direction:
                if data.value in line:
                    g.direction = Direction(data.value)
                    g.j = line.index(data.value)
                    g.i = r
            matrix.append(list(line.rstrip()))
            r += 1
        g.max_row = len(matrix)

        g.max_column = len(matrix[0])
    return matrix, g


if __name__ == "__main__":
    filename = sys.argv[1]
    lab_map, guard = read_input(filename)
    original_guard = deepcopy(guard)
    part_1(lab_map, guard)
    part_2(lab_map, original_guard)
