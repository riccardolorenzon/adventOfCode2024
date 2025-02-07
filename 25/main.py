import sys

from collections import namedtuple


Lock = namedtuple("Lock", "columns")
Key = namedtuple("Key", "columns")
COLUMNS = 5
ROWS = 7


def get_shape_tuple(shape: list[str]) -> tuple[int, int, int, int, int]:
    identity_char = shape[0][0]
    res = []
    for i in range(COLUMNS):
        column = "".join(
            [shape[j][i] for j in range(len(shape)) if shape[j][i] == identity_char]
        )
        if identity_char == "#":
            res.append(len(column.rstrip(".")))
        else:
            res.append(ROWS - len(column.rstrip("#")))
    return res


def map_key_lock(shape: list[str], keys: list[Key], locks: list[Lock]):
    if shape[0][0] == "#":
        locks.append(get_shape_tuple(shape))
    else:
        keys.append(get_shape_tuple(shape))


def read_input() -> tuple[list[Key], list[Lock]]:
    keys, locks = [], []
    shape = []

    with open(sys.argv[1]) as f:
        while line := f.readline():
            if line == "\n":
                map_key_lock(shape, keys, locks)
                shape = []
            else:
                shape.append(line.rstrip())
    map_key_lock(shape, keys, locks)
    return keys, locks


def get_matching_pairs(keys: list[Key], locks: list[Lock]) -> int:
    n_pairs = 0
    for key in keys:
        for lock in locks:
            for i in range(COLUMNS):
                if key[i] + lock[i] > ROWS:
                    break
            else:
                n_pairs += 1
    return n_pairs


def main():
    keys, locks = read_input()
    # part 1
    print(get_matching_pairs(keys, locks))


if __name__ == "__main__":
    main()
