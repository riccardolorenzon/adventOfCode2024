import sys
from typing import NamedTuple
import heapq


class Point(NamedTuple):
    x: int
    y: int


def read_input():
    grid_width = int(sys.argv[1])
    grid_height = int(sys.argv[2])
    grid = [["." for _ in range(grid_width)] for _ in range(grid_height)]
    max_amount_of_bytes = int(sys.argv[3])
    next_bytes = []
    with open(sys.argv[4]) as f:
        while line := f.readline().strip():
            if max_amount_of_bytes == 0:
                next_bytes.append(list(map(int, line.split(","))))
            else:
                x, y = list(map(int, line.split(",")))
                grid[y][x] = "#"
                max_amount_of_bytes -= 1
    return grid, next_bytes


def get_neighbors(_map: list[list[str]], node: Point) -> list[Point]:
    candidate_neighbors = [
        (node.x - 1, node.y),
        (node.x + 1, node.y),
        (node.x, node.y - 1),
        (node.x, node.y + 1),
    ]
    width = len(_map[0])
    height = len(_map)
    neighbors = []
    for n_x, n_y in candidate_neighbors:
        if n_x in range(0, width) and n_y in range(0, height) and _map[n_y][n_x] != "#":
            neighbors.append(Point(n_x, n_y))
    return neighbors


def shortest_path(_map: list[list[str]], start: Point, end: Point) -> int:
    # dijkstra
    distances = [[float("inf") for _ in range(len(_map[0]))] for _ in range(len(_map))]
    distances[start.y][start.x] = 0
    visited = set()
    heap = [(distances[start.y][start.x], start)]
    heapq.heapify(heap)

    while heap:
        _, node = heapq.heappop(heap)
        if node not in visited:
            visited.add(node)
            for n in get_neighbors(_map, node):
                if 1 + distances[node.y][node.x] < distances[n.y][n.x]:
                    distances[n.y][n.x] = 1 + distances[node.y][node.x]
                    heapq.heappush(heap, (distances[n.y][n.x], n))
    return distances[len(grid) - 1][len(grid[0]) - 1]


if __name__ == "__main__":
    grid, _ = read_input()
    # first part
    print(shortest_path(grid, Point(0, 0), Point(len(grid[0]) - 1, len(grid) - 1)))

    # second part
    grid, next_bytes = read_input()
    n_x, n_y = None, None
    while shortest_path(
        grid, Point(0, 0), Point(len(grid[0]) - 1, len(grid) - 1)
    ) != float("inf"):
        n_x, n_y = next_bytes.pop(0)
        grid[n_y][n_x] = "#"
    print(f"{n_x},{n_y}")
