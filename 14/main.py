import re
import sys

from time import sleep
from typing import List
from dataclasses import dataclass
from functools import reduce

REGEX_ROBOT_INPUT = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")


COLUMNS = int(sys.argv[2])
ROWS = int(sys.argv[3])


@dataclass
class Robot:
    v_x: int
    v_y: int

    x: int
    y: int

    def move(self):
        self.x = (self.x + self.v_x + COLUMNS) % COLUMNS
        self.y = (self.y + self.v_y + ROWS) % ROWS


def get_safety_factor(robots: List[Robot]) -> int:
    first_quadrant_x, first_quadrant_y = range(0, COLUMNS // 2), range(0, ROWS // 2)
    second_quadrant_x, second_quadrant_y = range((COLUMNS // 2) + 1, COLUMNS), range(
        0, ROWS // 2
    )
    third_quadrant_x, third_quadrant_y = range(0, COLUMNS // 2), range(
        (ROWS // 2) + 1, ROWS
    )
    fourth_quadrand_x, fourth_quadrant_y = range((COLUMNS // 2) + 1, COLUMNS), range(
        (ROWS // 2) + 1, ROWS
    )
    number_robots_per_quadrant = [0, 0, 0, 0]
    for robot in robots:
        if robot.x in first_quadrant_x and robot.y in first_quadrant_y:
            number_robots_per_quadrant[0] += 1
        if robot.x in second_quadrant_x and robot.y in second_quadrant_y:
            number_robots_per_quadrant[1] += 1
        if robot.x in third_quadrant_x and robot.y in third_quadrant_y:
            number_robots_per_quadrant[2] += 1
        if robot.x in fourth_quadrand_x and robot.y in fourth_quadrant_y:
            number_robots_per_quadrant[3] += 1

    return reduce(lambda x, y: x * y, number_robots_per_quadrant)


def display_robots(robots: List[Robot]):
    matrix = [["." for _ in range(COLUMNS)] for _ in range(ROWS)]
    for robot in robots:
        matrix[robot.y][robot.x] = "X"
    for line in matrix:
        print("".join(line))


def add_step(robots: List[Robot]):
    for _ in range(100):
        for robot in robots:
            robot.move()


def wait_till_tree(robots: list[Robot]):
    positions = set()
    i = 0
    while True:
        i += 1

        positions = set()
        [robot.move() for robot in robots for _ in range(1)]
        n_robots = len(robots)
        for robot in robots:
            position = (robot.x, robot.y)
            positions.add(position)
        if n_robots == len(positions):
            display_robots(robots)
            print(i)
            break


def clear():
    print("\n")


def read_input() -> List[Robot]:
    robots = []
    with open(sys.argv[1]) as f:
        while line := f.readline().strip():
            # p=0,4 v=3,-3
            g = REGEX_ROBOT_INPUT.match(line)
            robots.append(Robot(v_x=int(g[3]), v_y=int(g[4]), x=int(g[1]), y=int(g[2])))
    return robots


if __name__ == "__main__":
    robots = read_input()
    add_step(robots)
    print(get_safety_factor(robots))
    robots = read_input()
    wait_till_tree(robots)
