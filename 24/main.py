from __future__ import annotations

import sys

import dataclasses
import enum


def get_operator_func(operator: OperatorEnum):
    match (operator):
        case OperatorEnum.XOR:
            return lambda x, y: x ^ y
        case OperatorEnum.OR:
            return lambda x, y: x or y
        case OperatorEnum.AND:
            return lambda x, y: x and y
    raise Exception("Operator enum function is not mapped")


class OperatorEnum(enum.Enum):
    XOR = "XOR"
    OR = "OR"
    AND = "AND"


@dataclasses.dataclass(frozen=True)
class Variable:
    name: str
    value: int


@dataclasses.dataclass
class Operation:
    operand1: str
    operand2: str
    operation: OperatorEnum
    result_operand: str

    def perform(self, operand1_value: Variable, operand2_value: Variable) -> Variable:
        return Variable(
            self.result_operand,
            get_operator_func(self.operation)(
                operand1_value.value, operand2_value.value
            ),
        )


def read_input() -> tuple[dict[Variable], list[Operation]]:
    variables = {}
    operations = []

    with open(sys.argv[1]) as f:
        while line := f.readline().strip():
            name, value = line.split(":")
            variables[name.strip()] = Variable(name.strip(), int(value.strip()))
        while line := f.readline().strip():
            expression, result_operand = line.split(" -> ")
            operand1, operation, operand2 = expression.split()
            operations.append(
                Operation(operand1, operand2, OperatorEnum(operation), result_operand)
            )
    return variables, operations


def get_values(
    variables: dict[Variable], operations: list[Operation]
) -> dict[Variable]:
    while operations:
        operation = operations.pop()
        if (
            operation.operand1 in variables.keys()
            and operation.operand2 in variables.keys()
        ):
            # perform operation and store variable in variables
            variable = operation.perform(
                variables[operation.operand1], variables[operation.operand2]
            )
            variables[variable.name] = variable
        else:
            operations.insert(0, operation)
    return variables


def get_decimal_z_wires(variables: list[Variable]):
    variables_names_prefix_z = [
        variable_name for variable_name in variables.keys() if variable_name[0] == "z"
    ]
    variables_names_prefix_z.sort()
    position = 0
    result = 0
    for variable_name in variables_names_prefix_z:
        result += (2**position) * variables[variable_name].value
        position += 1
    return result


def main():
    variables, operations = read_input()
    variables = get_values(variables, operations)
    # part 1
    print(get_decimal_z_wires(variables))


if __name__ == "__main__":
    main()
