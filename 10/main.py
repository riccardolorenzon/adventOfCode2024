# the problem is to find how many trailheads, a trailhead is a route starting from 0 to 9, and sum the scores
# the score of a trailhead is the number of a 9s reachable from the start of the trailhead
# every step can be in any direction, except diagonal
# always uphill and max +1

# the idea is to start with bruteforce, for each 0 check how many 9s are reachable
# a 9 reachable via 2 different routes counts only once per trailhead
# the algorithm would use backpropagation, that means from each position trying each possible route,
# eventually stopping the route afterwards
import sys
from typing import List, Set


def read_input() -> List[List[int]]:
    filename = sys.argv[1]
    matrix = []
    with open(filename) as f:
        while line := f.readline().strip():
            matrix.append(list(line))
    return matrix


score_up = lambda matrix, i, j, visited_routes: get_score(
    matrix, i - 1, j, visited_routes
)
score_down = lambda matrix, i, j, visited_routes: get_score(
    matrix, i + 1, j, visited_routes
)
score_left = lambda matrix, i, j, visited_routes: get_score(
    matrix, i, j - 1, visited_routes
)
score_right = lambda matrix, i, j, visited_routes: get_score(
    matrix, i, j + 1, visited_routes
)

look_up = lambda matrix, i, j: matrix[i - 1][j] if i > 0 else None
look_down = lambda matrix, i, j: matrix[i + 1][j] if i < len(matrix) - 1 else None
look_left = lambda matrix, i, j: matrix[i][j - 1] if j > 0 else None
look_right = lambda matrix, i, j: matrix[i][j + 1] if j < len(matrix[0]) - 1 else None


def get_score(matrix: List[List[int]], i: int, j: int, visited_routes: Set) -> int:
    # check if one of the cells adjacent has matrix[i][j]+
    score = 0
    if matrix[i][j] == "9":
        if visited_routes is not None and (i, j) not in visited_routes:
            visited_routes.add((i, j))
            return 1
        elif visited_routes is None:
            return 1
    next_step = str(int(matrix[i][j]) + 1)
    if look_up(matrix, i, j) == next_step:
        score += score_up(matrix, i, j, visited_routes)
    if look_down(matrix, i, j) == next_step:
        score += score_down(matrix, i, j, visited_routes)
    if look_left(matrix, i, j) == next_step:
        score += score_left(matrix, i, j, visited_routes)
    if look_right(matrix, i, j) == next_step:
        score += score_right(matrix, i, j, visited_routes)
    return score


def get_trailheads_score(matrix: List[List[int]]) -> int:
    score = 0
    for i, row in enumerate(matrix):
        for j, _ in enumerate(row):
            if matrix[i][j] == "0":
                score += get_score(matrix, i, j, set())
    return score


def get_rating_score(matrix: List[List[int]]) -> int:
    score = 0
    for i, row in enumerate(matrix):
        for j, _ in enumerate(row):
            if matrix[i][j] == "0":
                score += get_score(matrix, i, j, None)
    return score


if __name__ == "__main__":
    matrix = read_input()
    print(get_trailheads_score(matrix))
    print(get_rating_score(matrix))
