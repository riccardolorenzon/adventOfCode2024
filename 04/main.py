XMAS = "XMAS"
SAMX = "SAMX"


def check_horizontal_line(matrix, i, j):
    res = 0
    # line is i, check if j+1, j+2, j+3 == XMAS, or j-1, j-2, j-3 == XMAS
    if "".join(matrix[i][j : min(j + 4, len(matrix[i]))]) == XMAS:
        res += 1
        print("found horizontal 1")
    if "".join(matrix[i][max(0, j - 3) : j + 1]) == SAMX:
        res += 1
        print("found horizontal 2")
    print(f"total horizonatl lines {res}")
    return res


def check_vertical_line(matrix, i, j):
    res = 0
    vertical_line = [matrix[x][j] for x in range(i, min(i + 4, len(matrix)))]
    if "".join(vertical_line) == XMAS:
        print("found vertical 1")
        res += 1
    vertical_line = [matrix[x][j] for x in range(max(i - 3, 0), i + 1)]
    if "".join(vertical_line) == SAMX:
        print("found vertical 2")
        res += 1

    print(f"total vertical lines {res}")
    return res


def check_diagonal_line(matrix, i, j):
    res = 0
    # 4
    diagonal_x = [x for x in range(i, min(i + 4, len(matrix)))]
    diagonal_y = [y for y in range(j, min(j + 4, len(matrix[i])))]
    diagonal = dict(zip(diagonal_x, diagonal_y))
    if "".join(matrix[x][y] for x, y in diagonal.items()) == XMAS:
        print("found 1")
        res += 1

    # 3
    diagonal_x = [x for x in range(i, min(i + 4, len(matrix)))]
    diagonal_y = [y for y in range(j, max(0, j - 4), -1)]
    diagonal = dict(zip(diagonal_x, diagonal_y))
    if "".join(matrix[x][y] for x, y in diagonal.items()) == XMAS:
        print("found 2")
        res += 1

    # 2
    diagonal_x = [x for x in range(max(i - 3, 0), i + 1)]
    diagonal_y = [y for y in range(min(j + 3, len(matrix[i]) - 1), j - 1, -1)]
    diagonal = dict(zip(diagonal_x, diagonal_y))
    if "".join(matrix[x][y] for x, y in diagonal.items()) == SAMX:
        print("found 3")
        res += 1

    # 1
    diagonal_x = [x for x in range(max(i - 3, 0), i + 1)]
    diagonal_y = [y for y in range(max(0, j - 3), j + 1)]
    diagonal = dict(zip(diagonal_x, diagonal_y))
    if "".join(matrix[x][y] for x, y in diagonal.items()) == SAMX:
        print("found 4")
        res += 1

    print(f"total diagonal lines {res}")
    return res


def part_1(matrix):
    occurences = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == "X":
                print(f"checking for coordinates {i, j}\n")
                occurences += check_horizontal_line(matrix, i, j)
                occurences += check_vertical_line(matrix, i, j)
                occurences += check_diagonal_line(matrix, i, j)
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
