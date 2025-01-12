# the first idea turned out to be not working and quite clumsy
# the approach then it's reconsidered
# we consider the plant map as a graph, and every plant
# the branches of the graph are between cells that are on the same line or column with distance of 1
import sys
from typing import NamedTuple
from dataclasses import dataclass
from typing import List, Generator


class Cell(NamedTuple):
    i: int
    j: int


def same_neighbors(i, j, plot_map: List[List[str]]) -> Generator:
    directions = [[-1, 0], [1, 0], [0, 1], [0, -1]]
    max_width = len(plot_map[0]) - 1
    max_height = len(plot_map) - 1
    for delta_i, delta_j in directions:
        if 0 <= i + delta_i <= max_height and 0 <= j + delta_j <= max_width:
            yield (i + delta_i, j + delta_j)


def same_plant_neighbors(i, j, plant, plot_map: List[List[str]]) -> Generator:
    for pos in same_neighbors(i, j, plot_map):
        if plot_map[pos[0]][pos[1]] == plant:
            yield (pos[0], pos[1])


def same_region_neighbors(i, j, region_id, plot_map: List[List[str]]) -> Generator:
    for pos in same_neighbors(i, j, plot_map):
        if plot_map[pos[0]][pos[1]] == region_id:
            yield (pos[0], pos[1])


@dataclass
class Region:
    region_id: int
    plant: str
    area: int
    perimeter: int


def read_input():
    with open(sys.argv[1]) as f:
        return [list(line.strip()) for line in f.readlines()]


def visited(plot_map, i, j):
    return isinstance(plot_map[i][j], int)


def traverse(plot_map):
    regions = []
    for i in range(len(plot_map)):
        for j in range(len(plot_map[0])):
            if not (visited(plot_map, i, j)):
                regions.append(process_region(plot_map, i, j, len(regions)))
    return regions


def process_region(plot_map: List[List[str]], i: int, j: int, region_id: int):
    # starting from the element i,j get all the neighbors with same plant
    # stop when there are no neighbors left
    neighbors = [Cell(i=i, j=j)]
    area = 0
    perimeter = 0
    plant = plot_map[i][j]
    while neighbors:
        next_cell = neighbors.pop(0)
        if visited(plot_map, next_cell.i, next_cell.j):
            continue
        plot_map[next_cell.i][next_cell.j] = region_id
        area += 1
        # 4 - edges with same region neighbors, multiplied by 2 because both position
        # need to have one edge removed
        perimeter += 4 - 2 * sum(
            1
            for _ in same_region_neighbors(
                next_cell.i, next_cell.j, region_id, plot_map
            )
        )

        neighbors.extend(
            map(
                lambda x: Cell(i=x[0], j=x[1]),
                list(same_plant_neighbors(next_cell.i, next_cell.j, plant, plot_map)),
            )
        )

    return Region(region_id, plot_map[i][j], area, perimeter)


def calculate_price(regions: List[Region]):
    price = 0
    for region in regions:
        price += region.area * region.perimeter
        print(f"{region.plant} {region.area} * {region.perimeter}")
    print(price)
    return price


if __name__ == "__main__":
    plot_map = read_input()
    regions = traverse(plot_map)
    calculate_price(regions)
