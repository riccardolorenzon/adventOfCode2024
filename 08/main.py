from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
import sys
from typing import List, Set


@dataclass
class Coords:
    i: int
    j: int

    def is_out(self, n, m) -> bool:
        return self.i < 0 or self.i >= n or self.j < 0 or self.j >= m

    def __eq__(self, other) -> bool:
        return self.i == other.i and self.j == other.j


def get_coords(matrix: List[List[str]]) -> Set:
    coords = defaultdict(list)
    for i, line in enumerate(matrix):
        for j, point in enumerate(line):
            if point != ".":
                coords[point].append(Coords(i, j))
    return coords


def read_input(filename: str) -> List[List[str]]:
    matrix = []
    with open(filename) as f:
        while line := f.readline():
            matrix.append(list(line.rstrip()))
    return matrix


def part_1(coords: Set, n: int, m: int, matrix) -> int:
    antinodes = 0
    visited_antinodes = set()
    for freq, coordinates in coords.items():
        for idx, coord in enumerate(coordinates):
            for other_coord in coordinates[idx + 1 :]:
                antinodes += count_antinodes(
                    coord, other_coord, n, m, visited_antinodes
                )
    return antinodes


def part_2(coords: Set, n: int, m: int, matrix) -> int:
    antinodes = 0
    visited_antinodes = set()
    for freq, coordinates in coords.items():
        for idx, coord in enumerate(coordinates):
            for other_coord in coordinates[idx + 1 :]:
                antinodes += count_antinodes_repeat(
                    coord, other_coord, n, m, visited_antinodes
                )
    for item in visited_antinodes:
        matrix[item[0]][item[1]] = "#"
    return antinodes


def count_antinodes(
    coord1: Coords, coord2: Coords, n: int, m: int, visited_antinodes: set
) -> int:
    antinodes = 0
    height = coord2.i - coord1.i
    width = coord2.j - coord1.j
    if 0 <= coord2.i + height < n and 0 <= coord2.j + width < m:
        if (coord2.i + height, coord2.j + width) not in visited_antinodes:
            visited_antinodes.add((coord2.i + height, coord2.j + width))
            antinodes += 1
    if 0 <= coord1.i - height < n and 0 <= coord1.j - width < m:
        if (coord1.i - height, coord1.j - width) not in visited_antinodes:
            visited_antinodes.add((coord1.i - height, coord1.j - width))
            antinodes += 1
    return antinodes


def count_antinodes_repeat(
    coord1: Coords,
    coord2: Coords,
    n: int,
    m: int,
    visited_antinodes: set,
) -> int:
    antinodes = 0
    height = coord2.i - coord1.i
    width = coord2.j - coord1.j
    multi = 0

    new_coord1 = Coords(coord1.i - multi * height, coord1.j - multi * width)
    new_coord2 = Coords(coord2.i + multi * height, coord2.j + multi * width)
    while not new_coord1.is_out(n, m) or not new_coord2.is_out(n, m):
        if not new_coord2.is_out(n, m):
            if (new_coord2.i, new_coord2.j) not in visited_antinodes:
                visited_antinodes.add((new_coord2.i, new_coord2.j))
                antinodes += 1
        if not new_coord1.is_out(n, m):
            if (new_coord1.i, new_coord1.j) not in visited_antinodes:
                visited_antinodes.add((new_coord1.i, new_coord1.j))
                antinodes += 1
        new_coord1 = Coords(coord1.i - multi * height, coord1.j - multi * width)
        new_coord2 = Coords(coord2.i + multi * height, coord2.j + multi * width)
        multi += 1
    return antinodes


if __name__ == "__main__":
    filename = sys.argv[1]
    # read input from file -> store in matrix
    # store in a dictionary with key -> frequency the list of coordinates
    # for each combination per frequency ->
    #   check if the antinodes fall within the boundary of the matrix
    matrix = read_input(filename)
    coords = get_coords(matrix)
    n = len(matrix)
    m = len(matrix[0])
    original_matrix = deepcopy(matrix)
    print(f"total number of antinodes is {part_1(coords, n, m, matrix)}")
    print(f"total number of antinodes is {part_2(coords, n, m, original_matrix)}")
