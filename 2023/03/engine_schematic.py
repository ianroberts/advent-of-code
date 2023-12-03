import re
from typing import TypeVar

T = TypeVar()


def input_matrix() -> list[str]:
    """
    Read the input file, extend any short lines with dots to the length of the longest
    one to make the schematic rectangular (this is not actually required for the given
    test data, as that matrix is rectangular to start with), then add a border of dots
    around the outside to avoid any strange edge effects in subsequent analysis.
    """
    with open("input", "r") as f:
        # Add leading and trailing dot to each line
        schematic: list[str] = [f".{line.strip()}." for line in f]

    longest_line = max(len(line) for line in schematic)
    for i in range(len(schematic)):
        if len(schematic[i]) < longest_line:
            schematic[i] += "." * (longest_line - len(schematic[i]))

    # Add "empty" (i.e. all dots) first and last lines to complete the border
    schematic.insert(0, "." * longest_line)
    schematic.append("." * longest_line)

    return schematic


def set_surrounding(matrix: list[list[T]], value: T, i: int, j: int) -> None:
    """
    In a given matrix, set the eight cells surrounding a given cell to a given value.
    :param matrix: the matrix
    :param value: the value to set in the matrix cells
    :param i: row number, must be between 1 and len(matrix)-2 inclusive, i.e. not on an edge
    :param j: column number, must be between 1 and len(matrix[i])-2 inclusive, i.e. not on an edge
    """
    matrix[i-1][j-1] = value
    matrix[i-1][j] = value
    matrix[i-1][j+1] = value
    matrix[i][j-1] = value
    matrix[i][j+1] = value
    matrix[i+1][j-1] = value
    matrix[i+1][j] = value
    matrix[i+1][j+1] = value


def sum_part_numbers() -> int:
    schematic = input_matrix()
    # Build a matching array of booleans for whether a digit in each position is
    # part of a part-number.  To do this, start with all False, then flip to True
    # the eight spots surrounding every symbol in the schematic
    part_number_positions: list[list[bool]] = [[False] * len(line) for line in schematic]
    symbol_regex = re.compile(r"[^0-9.]")
    for i in range(len(schematic)):
        for m in symbol_regex.finditer(schematic[i]):
            set_surrounding(part_number_positions, True, i, m.start())

    # Now look at all possible numbers and determine which ones are part numbers
    total = 0
    number_regex = re.compile(r"\d+")
    for i in range(len(schematic)):
        for m in number_regex.finditer(schematic[i]):
            if any(part_number_positions[i][j] for j in range(*m.span())):
                total += int(m.group())

    return total


# ---- Part 2 ----


def append_surrounding(matrix: list[list[list[T]]], value: T, row: int, start_col: int, end_col: int) -> None:
    """
    Given a matrix whose cells are lists, append the given value to all the cells surrounding
    a 1xN block of positions.  Assumes that start_col > 0 and end_col < len(matrix[row])
    :param matrix: the rectangular matrix, indexed first by row, then by column
    :param value: the value to append
    :param row: the row in the matrix (first index into matrix)
    :param start_col: first column, inclusive
    :param end_col: last column, *exclusive*
    """
    for pos in range(start_col-1, end_col+1):
        matrix[row-1][pos].append(value)
        matrix[row+1][pos].append(value)
    matrix[row][start_col-1].append(value)
    matrix[row][end_col].append(value)


def sum_gear_ratios() -> int:
    schematic = input_matrix()
    # Build an array of all the numbers "surrounding" each position - start with a matrix
    # the same size as the schematic, where each cell is itself an empty list
    surrounding_numbers: list[list[list[int]]] = [[[] for _ in range(len(line))] for line in schematic]

    # Now find all the numbers, and add each number to the list for all its surrounding cells
    number_regex = re.compile(r"\d+")
    for i in range(len(schematic)):
        for m in number_regex.finditer(schematic[i]):
            append_surrounding(surrounding_numbers, int(m.group()), i, m.start(), m.end())

    # now find every * in the original schematic that has _exactly two_ numbers in its
    # surrounding cells, calculate its ratio and sum up
    total_gear_ratios = 0
    for i in range(len(schematic)):
        star_pos = -1
        while (star_pos := schematic[i].find("*", star_pos+1)) >= 0:
            if len(surrounding_numbers[i][star_pos]) == 2:
                total_gear_ratios += surrounding_numbers[i][star_pos][0] * surrounding_numbers[i][star_pos][1]

    return total_gear_ratios


if __name__ == '__main__':
    print(f"Sum of part numbers: {sum_part_numbers()}")
    print(f"Total gear ratio: {sum_gear_ratios()}")