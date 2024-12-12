XMAS = "XMAS"
SAMX = "SAMX"

directions_diags = {
    "up_right": lambda i, j: (i - 1, j + 1),
    "right_down": lambda i, j: (i + 1, j + 1),
    "down_left": lambda i, j: (i + 1, j - 1),
    "up_left": lambda i, j: (i - 1, j - 1),
}

opposite_diags = {
    "up_right": "down_left",
    "right_down": "up_left",
    "down_left": "up_right",
    "up_left": "right_down",
}

directions = {
    "up": lambda i, j: (i - 1, j),
    "right": lambda i, j: (i, j + 1),
    "down": lambda i, j: (i + 1, j),
    "left": lambda i, j: (i, j - 1),
}


def check_line(matrix, coord, word_left, direction):
    i, j = coord[0], coord[1]
    if len(word_left) == 0:
        return True
    width = len(matrix[0])
    height = len(matrix)
    if i > height - 1 or j > width - 1 or i < 0 or j < 0:
        return False
    if matrix[i][j] == word_left[0]:
        return check_line(matrix, direction(i, j), word_left[1:], direction)
    else:
        return False


def part_1(matrix):
    occurences = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == "X":
                for _, direction in {**directions, **directions_diags}.items():
                    if check_line(matrix, direction(i, j), "MAS", direction):
                        occurences += 1

    print(f"Total number of occurences part 1 is {occurences}")


def part_2(matrix):
    # the idea is to intercept every 'A' and check if MS os SM is on each diag
    occurences = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == "A":
                if (
                    check_line(
                        matrix,
                        directions_diags["up_right"](i, j),
                        "MAS",
                        directions_diags[opposite_diags["up_right"]],
                    )
                    or check_line(
                        matrix,
                        directions_diags["up_right"](i, j),
                        "SAM",
                        directions_diags[opposite_diags["up_right"]],
                    )
                ) and (
                    check_line(
                        matrix,
                        directions_diags["right_down"](i, j),
                        "MAS",
                        directions_diags[opposite_diags["right_down"]],
                    )
                    or check_line(
                        matrix,
                        directions_diags["right_down"](i, j),
                        "SAM",
                        directions_diags[opposite_diags["right_down"]],
                    )
                ):
                    occurences += 1
    print(f"Total number of occurences part 2 is {occurences}")


def load_matrix():
    matrix = []
    with open("data.txt") as f:
        while line := f.readline():
            matrix.append([char for char in line.strip()])
    return matrix


if __name__ == "__main__":
    matrix = load_matrix()
    part_1(matrix)
    part_2(matrix)
