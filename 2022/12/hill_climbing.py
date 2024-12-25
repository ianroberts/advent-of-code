from aoc_common.heapdict import heapdict
from aoc_common.grid import Cell


def parse_input():
    heights: list[list[int]] = []
    start: Cell
    end: Cell
    with open("input", "r") as f:
        for r, line in enumerate(f):
            line = line.strip()
            row = [50]
            heights.append(row)
            for c, char in enumerate(line):
                if char == "S":
                    start = Cell(r+1, c+1)
                    char = "a"
                elif char == "E":
                    end = Cell(r+1, c+1)
                    char = "z"

                row.append(ord(char) - ord('a'))
            row.append(50)

    heights.insert(0, [50 for _ in heights[0]])
    heights.append([50 for _ in heights[-1]])

    return heights, start, end


def single_source_shortest_paths(start: Cell, heights: list[list[int]]) -> dict[Cell, int]:
    """
    Find all the shortest path lengths from a given start point to every
    reachable cell in the given grid of heights.
    :return: dict mapping each reachable Cell to its distance from the start
    """
    def neighbours(src: Cell) -> list[Cell]:
        my_height = src.of(heights)
        return [c for c in src.neighbours() if c.of(heights) - my_height <= 1]

    open_list = heapdict()
    open_list[start] = 0
    costs: dict[Cell, int] = {start: 0}
    closed_list: set[Cell] = set()

    while len(open_list):
        node, f_node = open_list.popitem()
        closed_list.add(node)

        for child in neighbours(node):
            if child in closed_list:
                continue
            child_cost = costs[node] + 1
            if child not in costs or child_cost < costs[child]:
                costs[child] = child_cost
                open_list[child] = costs[child]

    return costs

def part1():
    heights, start, end = parse_input()

    costs = single_source_shortest_paths(start, heights)
    print(f"Steps in shortest path: {costs[end]}")


def part2():
    heights, start, end = parse_input()

    # This time we're starting from the end node and tracing paths downhill.
    # This is equivalent to tracing uphill paths on a map where all the heights
    # apart from the boundary ring around the outside edge are swapped in sign
    # (so the E cell is the *lowest* point in the resulting grid)
    for r in range(len(heights)):
        for c in range(len(heights[r])):
            if heights[r][c] != 50:
                heights[r][c] = -heights[r][c]

    costs = single_source_shortest_paths(end, heights)

    shortest_from_a = min(costs.get(Cell(r, c), 10000000000000) for r in range(len(heights)) for c in range(len(heights[0])) if heights[r][c] == 0)
    print(f"Shortest path from any a: {shortest_from_a}")



if __name__ == "__main__":
    part1()
    part2()