from dataclasses import dataclass
import sys
import enum
from itertools import product


class Operator(enum.Enum):
    PLUS = lambda x, y: (x + y)
    MULTIPLY = lambda x, y: (x * y)
    CONCAT = lambda x, y: int(str(x) + str(y))


@dataclass
class Operation:
    result: int = 0
    operands: list[int] = None

    def is_valid(self, concat=False) -> bool:
        possible_operations = "01" if not concat else "012"
        operator_combinations = product(
            possible_operations, repeat=len(self.operands) - 1
        )
        for operator_combination in operator_combinations:
            partial_result, i = self.operands[0], 1
            for operator in operator_combination:
                match (operator):
                    case "0":
                        partial_result = Operator.PLUS(partial_result, self.operands[i])
                    case "1":
                        partial_result = Operator.MULTIPLY(
                            partial_result, self.operands[i]
                        )
                    case "2":
                        partial_result = Operator.CONCAT(
                            partial_result, self.operands[i]
                        )
                i += 1
                if partial_result > self.result:
                    break

            if partial_result == self.result:
                return True
        return False


def part_1(operations: list[Operation]):
    result = 0
    for operation in operations:
        if operation.is_valid():
            result += operation.result
    print(f"The final sum of results for valid operations is {result}")


def part_2(operations: list[Operation]):
    result = 0
    for operation in operations:
        if operation.is_valid(concat=True):
            result += operation.result
    print(f"The final sum of results for valid operations is {result}")


def read_input(filename: str) -> list[list[int]]:
    operations = []
    with open(filename) as f:
        while line := f.readline():
            line = line.rstrip()
            operation = Operation(result=int(line.split(":")[0]))
            operation.operands = list(map(int, line.split(":")[1].strip().split(" ")))
            operations.append(operation)
    return operations


if __name__ == "__main__":
    filename = sys.argv[1]
    operations = read_input(filename)
    part_1(operations)
    part_2(operations)
