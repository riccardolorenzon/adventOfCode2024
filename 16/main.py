import sys
import enum
from typing import NamedTuple
import heapq
import dataclasses


class Direction(enum.Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    DOWN = "DOWN"
    UP = "UP"


class Position(NamedTuple):
    x: int
    y: int


@dataclasses.dataclass(frozen=True, order=True)
class RPosition:
    x: int
    y: int
    direction: Direction
    cost: int = 0

    def find_neighbors_positions(self):
        match (self.direction):
            case Direction.LEFT:
                return [
                    RPosition(self.x, self.y - 1, Direction.UP, 1000),
                    RPosition(self.x - 1, self.y, Direction.LEFT, 0),
                    RPosition(self.x, self.y + 1, Direction.DOWN, 1000),
                ]
            case Direction.RIGHT:
                return [
                    RPosition(self.x, self.y - 1, Direction.UP, 1000),
                    RPosition(self.x + 1, self.y, Direction.RIGHT, 0),
                    RPosition(self.x, self.y + 1, Direction.DOWN, 1000),
                ]
            case Direction.UP:
                return [
                    RPosition(self.x, self.y - 1, Direction.UP, 0),
                    RPosition(self.x + 1, self.y, Direction.RIGHT, 1000),
                    RPosition(self.x - 1, self.y, Direction.LEFT, 1000),
                ]
            case Direction.DOWN:
                return [
                    RPosition(self.x, self.y + 1, Direction.DOWN, 0),
                    RPosition(self.x + 1, self.y, Direction.RIGHT, 1000),
                    RPosition(self.x - 1, self.y, Direction.LEFT, 1000),
                ]


def find_start_end(_map: list[list[str]]) -> list[Position]:
    pos = [None] * 2
    for i in range(len(_map)):
        for j in range(len(_map[0])):
            if _map[i][j] == "S":
                pos[0] = Position(j, i)
            if _map[i][j] == "E":
                pos[1] = Position(j, i)
    return pos


def read_input():
    _map = []
    with open(sys.argv[1]) as f:
        while line := f.readline().strip():
            _map.append(list(line))
    return _map


def find_lowest_path_s_e(_map: list[list[str]]) -> int:
    pos_s, pos_e = find_start_end(_map)
    print(f"{pos_s} - {pos_e}")

    # scores will contain, for each i,j, the lowest cost to get to i,j from S
    scores = [[float("inf") for _ in range(len(_map[0]))] for _ in range(len(_map))]
    scores[pos_s.y][pos_s.x] = 0
    # visited contains visited (i,j) of _map
    visited = set()

    # pq is a priority queue, we store (distance, RPosition)
    # first node to store is S
    pq = [(0, RPosition(pos_s.x, pos_s.y, Direction.RIGHT, 0))]
    heapq.heapify(pq)

    # while there are items in pq, we extract the one with lowest score, calculate distance from the neighbors, and store the new items in pq
    while pq:
        cost, node = heapq.heappop(pq)

        neighbors = node.find_neighbors_positions()
        for neighbor in neighbors:
            if neighbor.x not in range(len(_map[0])) or neighbor.y not in range(
                len(_map)
            ):
                continue

            if neighbor not in visited:
                visited.add(neighbor)
                if _map[neighbor.y][neighbor.x] != "#":
                    tentative_lowest_distance = neighbor.cost + cost + 1
                    if tentative_lowest_distance < scores[neighbor.y][neighbor.x]:
                        scores[neighbor.y][neighbor.x] = tentative_lowest_distance
                        heapq.heappush(pq, (tentative_lowest_distance, neighbor))
    for line in scores:
        print(line)
    return scores[pos_e.y][pos_e.x]


if __name__ == "__main__":
    _map = read_input()
    print(find_lowest_path_s_e(_map))
    for line in _map:
        print("".join(line))
