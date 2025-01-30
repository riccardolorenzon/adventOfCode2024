from typing import NamedTuple
import sys
import heapq
from collections import defaultdict


class Pos(NamedTuple):
    x: int
    y: int


def get_start_and_end_points(_map: list[list[str]]) -> tuple[Pos, Pos]:
    pos_s, pos_e = None, None
    for i in range(len(_map)):
        for j in range(len(_map[0])):
            match _map[i][j]:
                case "S":
                    pos_s = Pos(j, i)
                case "E":
                    pos_e = Pos(j, i)
                case _:
                    pass
            if pos_s and pos_e:
                return (pos_s, pos_e)
    raise Exception("S or E not found")


def read_input() -> list[list[str]]:
    _map = []
    with open(sys.argv[1]) as f:
        while line := f.readline():
            _map.append(list(line.strip()))
    return _map


def shortest_distances(_map: list[list[str]], pos_s: Pos, pos_e: Pos) -> dict[Pos, int]:
    # return a dict with the distances from node pos to pos_e
    scores = defaultdict(lambda: float("inf"))
    scores[pos_s] = 0
    heap = [(0, pos_s)]
    heapq.heapify(heap)
    visited = set()

    while heap:
        node = heapq.heappop(heap)[1]
        if node in visited:
            continue
        else:
            visited.add(node)
            # get neighbors of node and update scores(if score not in scores -> inf), then push the neighbors on the heap and continue
            for neighbor in get_neighbors(node, len(_map[0]), len(_map), _map):
                if scores.get(neighbor) is None:
                    scores[neighbor] = 1 + scores[node]
                else:
                    if scores[node] + 1 < scores[neighbor]:
                        scores[neighbor] = scores[node] + 1
                heapq.heappush(heap, (scores[neighbor], neighbor))
    return scores


def is_pos_valid(pos: Pos, width: int, height: int, _map: list[list[str]]) -> bool:
    if pos.x not in range(0, width):
        return False
    if pos.y not in range(0, height):
        return False
    if _map[pos.y][pos.x] == "#":
        return False
    return True


def get_neighbors(node: Pos, width: int, height: int, _map: list[list[str]]):
    neighbors_pos = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for x, y in neighbors_pos:
        candidate_neighbor = Pos(node.x + x, node.y + y)
        if is_pos_valid(candidate_neighbor, width, height, _map):
            yield candidate_neighbor


def shortest_path(
    _map: list[list[str]], pos_s: Pos, pos_e: Pos, scores: dict[Pos, int]
) -> dict[Pos, object]:
    # return an ordered dict with the shortest path to pos_e
    path = {pos_e: None}
    node = pos_e
    while node != pos_s:
        for neighbor in get_neighbors(node, len(_map[0]), len(_map), _map):
            if scores[neighbor] + 1 == scores[node]:
                path[neighbor] = None
                node = neighbor
    return path


def gain_crossing_wall(
    _map: list[list[str]],
    wall_pos: Pos,
    scores: dict[Pos, int],
    save: int,
) -> bool:
    # if at least one of the nodes in the shortest path is next to the wall
    neighbors = get_neighbors(wall_pos, len(_map[0]), len(_map), _map)
    gain = 0
    for neighbor in neighbors:
        for other in neighbors:
            if neighbor == other:
                continue
            partial_gain = abs(scores[neighbor] - scores[other]) - 2
            if partial_gain != float("inf"):
                gain = max(gain, partial_gain)
    if gain >= save:
        return True
    return False


def get_cheats(_map, scores: dict[Pos, int], save) -> int:
    cheats = 0
    for i in range(len(_map)):
        for j in range(len(_map[0])):
            if _map[i][j] != "#":
                continue
            if gain_crossing_wall(_map, Pos(j, i), scores, save):
                cheats += 1
    return cheats


def main():
    _map = read_input()
    pos_s, pos_e = get_start_and_end_points(_map)
    print(f"Starting point: {pos_s}, ending point {pos_e}")
    scores = shortest_distances(_map, pos_s, pos_e)
    picoseconds_no_cheat = scores[pos_e]
    print(picoseconds_no_cheat)
    path = shortest_path(_map, pos_s, pos_e, scores)
    for p in path.keys():
        _map[p.y][p.x] = red("O")
    for line in _map:
        print("".join(line))
    cheats = get_cheats(_map, scores, 100)
    print(f"total number of cheats {cheats}")


def red(s):
    start = "\033[1;31m"
    end = "\033[0;0m"
    return f"{start}{s}{end}"


if __name__ == "__main__":
    main()
