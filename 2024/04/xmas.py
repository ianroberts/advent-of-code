def load_data():
    with open("input", "r") as f:
        return [l.strip() for l in f]


# (row, column) differences that move you one step in each of the eight
# directions E, SE, S, SW, W, NW, N, NE
DIRECTIONS = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
XMAS = "XMAS"


def num_xmas_from(lines: list[str], r: int, c: int) -> int:
    """
    Count the number of "XMAS" words that start from the given row/column location
    radiating in any of the eight directions.
    """
    if lines[r][c] != "X":
        return 0

    num = 0
    for dr, dc in DIRECTIONS:
        if r + (3 * dr) not in range(len(lines)) or c + (3 * dc) not in range(len(lines[0])):
            continue

        if any(lines[r + n * dr][c + n * dc] != XMAS[n] for n in range(1, 4)):
            continue

        num += 1

    return num


MS_SM = ("MS", "SM")


def num_crossing_mas_from(lines: list[str], r: int, c: int) -> int:
    """
    Determine whether the given location is the A at the centre of two crossing "MAS"
    words.

    :return: 1 if it is, 0 if not
    """
    if lines[r][c] != "A":
        return 0

    if r < 1 or c < 1 or r > len(lines) - 2 or c > len(lines[0]) - 2:
        return 0

    if (lines[r - 1][c - 1] + lines[r + 1][c + 1]) in MS_SM and (lines[r + 1][c - 1] + lines[r - 1][c + 1]) in MS_SM:
        return 1

    return 0


def find_words():
    lines = load_data()
    rows = len(lines)
    cols = len(lines[0])

    total_xmas = sum(num_xmas_from(lines, r, c) for r in range(rows) for c in range(cols))
    print(f"Total number of XMAS words: {total_xmas}")

    total_crossing = sum(num_crossing_mas_from(lines, r, c) for r in range(rows) for c in range(cols))
    print(f"Total crossing MAS: {total_crossing}")


if __name__ == "__main__":
    find_words()
