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


def same_plant_neighbors_corners(
    i, j, plant, region_id, plot_map: List[List[str]]
) -> int:
    neighbors = []
    for pos in same_neighbors(i, j, plot_map):
        if plot_map[pos[0]][pos[1]] == plant or plot_map[pos[0]][pos[1]] == region_id:
            neighbors.append(pos)
    print(neighbors)
    print(f"for {i}-{j} number of common neighbors is {len(neighbors)}")
    if len(neighbors) >= 3:
        return 0
    if len(neighbors) == 1:
        return 2
    if len(neighbors) == 2:
        pos1 = neighbors[0]
        pos2 = neighbors[1]
        if pos1[0] != pos2[0] and pos1[1] != pos2[1]:
            return 1
        else:
            return 0
    return 4


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
    corners: int


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
                regions.append(
                    process_region_area_perimeter(plot_map, i, j, len(regions))
                )
    return regions


def process_region_area_perimeter(
    plot_map: List[List[str]], i: int, j: int, region_id: int
):
    # starting from the element i,j get all the neighbors with same plant
    # stop when there are no neighbors left
    neighbors = [Cell(i=i, j=j)]
    area = 0
    perimeter = 0
    plant = plot_map[i][j]
    corners = 0
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
        # corners -> number of corners === number of sides
        # where corner ->
        # 1 neighbor same plant -> 2 corners
        # 2 neighbors same plant on perpendicolar directions -> 1 corner
        # 2 neighbors same plant on opposite directions -> 0 corner
        # 3 neighbors + -> 0 corner
        corners += same_plant_neighbors_corners(
            next_cell.i, next_cell.j, plant, region_id, plot_map
        )
        print(f"for { next_cell.i}-{ next_cell.j} number of corners is {corners}")
        neighbors.extend(
            map(
                lambda x: Cell(i=x[0], j=x[1]),
                list(same_plant_neighbors(next_cell.i, next_cell.j, plant, plot_map)),
            )
        )

    return Region(region_id, plot_map[i][j], area, perimeter, corners)


def calculate_price(regions: List[Region]):
    price = 0
    price_discounted = 0
    for region in regions:
        price += region.area * region.perimeter
        price_discounted += region.area * region.corners
        # print(f"{region.plant} {region.area} * {region.perimeter}")
        print(f"{region.plant} {region.area} * {region.corners}")
    print(price)
    print(price_discounted)
    return price


if __name__ == "__main__":
    plot_map = read_input()
    regions = traverse(plot_map)
    calculate_price(regions)
