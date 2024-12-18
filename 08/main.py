from collections import defaultdict
from dataclasses import dataclass
import sys
from typing import List, Set


@dataclass
class Coords:
    i: int
    j: int


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
    for freq, coordinates in coords.items():
        for idx, coord in enumerate(coordinates):
            for other_coord in coordinates[idx + 1 :]:
                antinodes += count_antinodes(coord, other_coord, n, m, matrix)
    return antinodes


def count_antinodes(coord1: Coords, coord2: Coords, n: int, m: int, matrix) -> int:
    antinodes = 0
    height = abs(coord2.i - coord1.i)
    width = abs(coord2.j - coord1.j)
    if coord2.j >= coord1.j:
        # diagonal is DESC
        if coord1.i - height >= 0 and coord1.j - width >= 0:
            if matrix[coord1.i - height][coord1.j - width] != "#":
                matrix[coord1.i - height][coord1.j - width] = "#"
                antinodes += 1
        if coord2.i + height < n and coord2.j + width < m:
            if matrix[coord2.i + height][coord2.j + width] != "#":
                matrix[coord2.i + height][coord2.j + width] = "#"
                antinodes += 1
    else:
        # diagonal is ASC
        if coord1.i - height >= 0 and coord1.j + width < m:
            if matrix[coord1.i - height][coord1.j + width] != "#":
                matrix[coord1.i - height][coord1.j + width] = "#"
                antinodes += 1
        if coord2.i + height < n and coord2.j - width >= 0:
            if matrix[coord2.i + height][coord2.j - width] != "#":
                matrix[coord2.i + height][coord2.j - width] = "#"
                antinodes += 1
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
    print(f"total number of antinodes is {part_1(coords, n, m, matrix)}")
    for line in matrix:
        print("".join(line))
