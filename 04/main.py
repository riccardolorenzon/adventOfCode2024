XMAS = "XMAS"
SAMX = "SAMX"

directions = {
    "up": lambda i, j: (i - 1, j),
    "uo_right": lambda i, j: (i - 1, j + 1),
    "right": lambda i, j: (i, j + 1),
    "right_down": lambda i, j: (i + 1, j + 1),
    "down": lambda i, j: (i + 1, j),
    "down_left": lambda i, j: (i + 1, j - 1),
    "left": lambda i, j: (i, j - 1),
    "up_left": lambda i, j: (i - 1, j - 1),
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
                print(f"checking for coordinates {i, j}\n")
                for _, direction in directions.items():
                    if check_line(matrix, direction(i, j), "MAS", direction):
                        occurences += 1
                print("\n")

    print(f"Total number of occurences is {occurences}")


def part_2():
    pass


def load_matrix():
    matrix = []
    with open("data.txt") as f:
        while line := f.readline():
            matrix.append([char for char in line.strip()])
    return matrix


if __name__ == "__main__":
    matrix = load_matrix()
    part_1(matrix)
