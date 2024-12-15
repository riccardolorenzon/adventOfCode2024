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


def part_1(lab_map: List[List[str]], guard: Guard) -> int:
    steps = 0
    try:
        while True:
            if lab_map[guard.i][guard.j] == "#":
                guard.previous()
                guard.turn()
            else:
                if lab_map[guard.i][guard.j] != "X":
                    steps += 1
                lab_map[guard.i][guard.j] = "X"
            guard.next()

    except StopIteration as e:
        print("exit!")
    finally:
        print(f"total number of steps {steps}")


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
    part_1(lab_map, guard)
