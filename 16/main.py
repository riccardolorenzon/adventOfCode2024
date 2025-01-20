import enum
import sys
from copy import deepcopy
import dataclasses


class Direction(enum.Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    DOWN = "DOWN"
    UP = "UP"


def map_movement(x: int, y: int, direction: Direction) -> tuple[int, int]:
    match (direction):
        case Direction.LEFT:
            return (x - 1, y)
        case Direction.RIGHT:
            return (x + 1, y)
        case Direction.DOWN:
            return (x, y + 1)
        case Direction.UP:
            return (x, y - 1)


@dataclasses.dataclass
class Robot:
    x: int
    y: int


def map_direction(symbol: str) -> Direction:
    match (symbol):
        case "<":
            return Direction.LEFT
        case "^":
            return Direction.UP
        case ">":
            return Direction.RIGHT
        case "v":
            return Direction.DOWN
    raise Exception(f"Unmapped symbol {symbol}")


def read_input() -> tuple[list[list[str]], list[Direction]]:
    # returns map, list of steps

    _map = []
    steps = []
    with open(sys.argv[1]) as f:
        line = f.readline().strip()
        while line != "":
            _map.append(list(line))
            line = f.readline().strip()
        for line in f.read().splitlines():
            for step in line:
                steps.append(map_direction(step))
        return _map, steps


def find_robot(_map: list[list[str]]) -> tuple[int, int]:
    for i in range(len(_map)):
        for j in range(len(_map[0])):
            if _map[i][j] == "@":
                return Robot(i, j)
    raise Exception("Robot not found")


def calculate_value(_map: list[list[str]]) -> int:
    sum_gps_coords = 0
    for i in range(len(_map)):
        for j in range(len(_map[0])):
            if _map[i][j] == "O":
                sum_gps_coords += (100 * i) + j
    return sum_gps_coords


def process_steps(_map: list[list[str]], directions: list[Direction]) -> None:
    robot = find_robot(_map)
    for direction in directions:
        # print(f"moving to direction {direction}")
        move_robot(_map, direction, robot)
        # for line in _map:
        #    print(line)
    return


def next_position(x, y, direction: Direction):
    next_x, next_y = map_movement(x, y, direction)
    return (next_x, next_y)


def move_robot(_map: list[list[str]], direction: Direction, robot: Robot) -> None:
    # [@.O.] -> [.@O.] [@O..] -> [.@O.]
    # [.@00000.] -> [..@00000] -> always one box and the robot to move
    next_x, next_y = next_position(robot.x, robot.y, direction)
    # print(f"next position: {next_x} {next_y} from {robot.x} {robot.y}")
    while next_x in range(0, len(_map[0])) and next_y in range(0, len(_map)):
        match _map[next_y][next_x]:
            case ".":
                _map[robot.y][robot.x] = "."
                if abs(next_x - robot.x) <= 1 and abs(next_y - robot.y) <= 1:
                    # only one step, no obastacles involved
                    _map[next_y][next_x] = "@"
                else:
                    _map[next_y][next_x] = "O"
                    next_x, next_y = next_position(robot.x, robot.y, direction)
                    _map[next_y][next_x] = "@"
                robot.x = next_x
                robot.y = next_y
                return
            case "O":
                next_x, next_y = next_position(next_x, next_y, direction)
            case "#":
                break


def widen_map(_map: list[list[str]]):
    _new_map = [[] for _ in range(len(_map))]
    for i in range(len(_map)):
        for j in range(len(_map[0])):
            if _map[i][j] == "O":
                _new_map[i].extend(["[", "]"])
            elif _map[i][j] != "@":
                _new_map[i].extend([_map[i][j], _map[i][j]])
            else:
                _new_map[i].extend(["@", "."])
    for line in _new_map:
        print("".join(line))
    return _new_map


if __name__ == "__main__":
    _map, directions = read_input()
    process_steps(deepcopy(_map), directions)
    print(calculate_value(_map))
    widen_map(_map)
