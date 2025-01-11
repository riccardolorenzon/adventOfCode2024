from __future__ import annotations

import sys
import itertools


from dataclasses import dataclass
from typing import List
import uuid


@dataclass
class Cell:
    i: int
    j: int
    plant: str
    width: int
    height: int
    region: Region = None
    neighbor_up: Cell = None
    neighbor_down: Cell = None
    neighbor_left: Cell = None
    neighbor_right: Cell = None

    @property
    def neighbors(self):
        neighbors = [
            self.neighbor_up,
            self.neighbor_down,
            self.neighbor_left,
            self.neighbor_right,
        ]

        return neighbors

    def partial_perimeter(self) -> int:
        p = 0
        if self.i == 0 or self.i == self.width:
            p += 1
        if self.j == 0 or self.j == self.height:
            p += 1
        neighbors = [
            self.neighbor_down,
            self.neighbor_left,
            self.neighbor_right,
            self.neighbor_up,
        ]
        for neighbor in neighbors:
            if neighbor and neighbor.plant != self.plant:
                p += 1
        return p

    def __repr__(self):
        return f"{self.region.group[:5]}" if self.region else "no-region"


@dataclass
class Region:
    id: str
    plant: str
    area: int = 0
    perimeter: int = 0
    group: str = None


regions = []


def read_input() -> List[List[str]]:
    plot_map = []
    filename = sys.argv[1]
    with open(filename) as f:
        while line := f.readline().rstrip():
            plot_map.append(list(line))

    return plot_map


def create_cell_plot_map(plot_map: List[List[str]]) -> List[List[Cell]]:
    for i, line in enumerate(plot_map):
        for j, _ in enumerate(line):
            plot_map[i][j] = Cell(
                i=i,
                j=j,
                plant=plot_map[i][j],
                width=len(plot_map) - 1,
                height=len(plot_map[0]) - 1,
            )
    return plot_map


def next_neighbor(i: int, j: int, height, width):
    neighbors = []
    if i > 0:
        neighbors.append((i - 1, j))
    else:
        neighbors.append((None, None))
    if i < height - 1:
        neighbors.append((i + 1, j))
    else:
        neighbors.append((None, None))
    if j > 0:
        neighbors.append((i, j - 1))
    else:
        neighbors.append((None, None))
    if j < width - 1:
        neighbors.append((i, j + 1))
    else:
        neighbors.append((None, None))
    yield from neighbors


def print_plot_map(plot_map: List[Cell]):
    for line in plot_map:
        print(line)


def map_area(plot_map: List[List[Cell]]):
    def get_neighbors_same_plant(i: int, j: int, plant: str) -> List[Cell]:
        neighbors = []
        for next_i, next_j in next_neighbor(i, j, len(plot_map), len(plot_map[0])):
            if (
                next_i is not None
                and plot_map[next_i][next_j].plant == plant
                and plot_map[next_i][next_j].region is not None
            ):
                neighbors.append(plot_map[next_i][next_j])
        return neighbors

    for i, line in enumerate(plot_map):
        for j, _ in enumerate(line):
            if plot_map[i][j].region is None:

                neighbors_same_plant = get_neighbors_same_plant(
                    i, j, plot_map[i][j].plant
                )
                if len(neighbors_same_plant) != 0:
                    # if multiple elements, merge region in case
                    plot_map[i][j].region = neighbors_same_plant[0].region
                    plot_map[i][j].region.area += 1
                    candidate_region = neighbors_same_plant[0].region
                    for n in neighbors_same_plant:
                        if n.region != candidate_region:
                            n.region.group = candidate_region.group
                else:
                    group_id = str(uuid.uuid4())
                    region = Region(
                        id=str(uuid.uuid4()),
                        plant=plot_map[i][j].plant,
                        area=1,
                        group=group_id,
                    )
                    regions.append(region)
                    # new Region
                    plot_map[i][j].region = region
    print_plot_map(plot_map)
    return plot_map


def map_perimeter(plot_map: List[List[Cell]]):
    for i, line in enumerate(plot_map):
        for j, _ in enumerate(line):
            neighbors = list(next_neighbor(i, j, len(plot_map), len(plot_map[0])))
            plot_map[i][j].neighbor_up = (
                plot_map[neighbors[0][0]][neighbors[0][1]]
                if neighbors[0][0] is not None
                else None
            )
            plot_map[i][j].neighbor_down = (
                plot_map[neighbors[1][0]][neighbors[1][1]]
                if neighbors[1][0] is not None
                else None
            )
            plot_map[i][j].neighbor_left = (
                plot_map[neighbors[2][0]][neighbors[2][1]]
                if neighbors[2][0] is not None
                else None
            )
            plot_map[i][j].neighbor_right = (
                plot_map[neighbors[3][0]][neighbors[3][1]]
                if neighbors[3][0] is not None
                else None
            )
            plot_map[i][j].region.perimeter += plot_map[i][j].partial_perimeter()
    return plot_map


def sum_regions():
    total = 0
    regions.sort(key=lambda x: x.plant)
    for region_group in itertools.groupby(
        sorted(regions, key=lambda x: x.group), lambda x: x.group
    ):
        group_area = 0
        group_perimeter = 0
        plant = None
        a = list(region_group[1])
        for region in a:
            group_area += region.area
            plant = region.plant
            group_perimeter += region.perimeter
        print(f"total for area {plant} {group_area} * {group_perimeter}")
        total += group_area * group_perimeter
    print(total)


# the idea is to start from a plot, and determine the region
# then proceed to its neighbors, and see
# - the region is the same?
# - the region is different
# each region is updated on its area and parameter by the plots

# how to identify which region a plot belongs to?
# keep a list of the 4 neighbors of each cell?
# no neighbors and neighbors without a region -> add new region
# one neighbor has same plant and region initialised -> get the region name

if __name__ == "__main__":
    plot_map = read_input()
    cell_plot_map = create_cell_plot_map(plot_map)
    map_area(cell_plot_map)
    map_perimeter(cell_plot_map)
    sum_regions()
