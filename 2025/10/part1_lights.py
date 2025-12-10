import re
from collections import namedtuple
from typing import Iterable

from aoc_common.heapdict import heapdict

LINE_PATTERN = re.compile(r"^\[(?P<target>[.#]+)] (?P<buttons>\(.*\)) \{(?P<jolts>.*)}")
BUTTON_PATTERN = re.compile(r"\((.*?)\)")

Machine = namedtuple("Machine", ["num_lights", "target", "buttons"])

def load_input():
    with open("input", "r") as f:
        machines = []
        for line in f:
            line = line.strip()
            m = LINE_PATTERN.match(line)
            if not m:
                raise ValueError(f"Invalid input line: {line}")

            # represent each target as a binary number with 1s for # and
            # 0s for . - technically this is flipped as the leftmost character
            # in the ...###.#. string is the least significant bit and the
            # rightmost is the most significant
            target = 0
            for i, ch in enumerate(m.group("target")):
                if ch == "#":
                    target |= 1 << i

            # represent each button similarly - as a binary number where bit
            # n is 1 if the button definition includes light n and 0 otherwise
            buttons = []
            for b in BUTTON_PATTERN.findall(m.group("buttons")):
                buttons.append(sum(2**int(l) for l in b.split(",")))

            # ignore the jolts for part 1

            machines.append(Machine(num_lights=len(m.group("target")), target=target, buttons=buttons))

    return machines


def cheapest_path(start: int, end: int, buttons: Iterable[int]):
    """
    Dijkstra to find the shortest path from start to end assuming all edges
    "cost" 1 unit.
    """

    # Use a heapdict for the unvisited list so the next node to be processed
    # is always the one with the lowest cost path from the start
    open_list = heapdict()
    # closed_list is the set of nodes we have completely visited
    closed_list: set[int] = set()
    # costs is the total cost of the cheapest path so far found to each node
    # (including the fully visited ones)
    costs: dict[int, int] = {}

    # Initial conditions - we're starting from the start node, and its
    # distance from the start node is (obviously) zero
    open_list[start] = 0
    costs[start] = 0

    while len(open_list):
        node, dist_node = open_list.popitem()
        closed_list.add(node)

        if node == end:
            # we have reached the goal
            return costs[end]

        for button in buttons:
            child = node ^ button
            if child in closed_list:
                continue
            child_cost = costs[node] + 1
            if child not in costs or child_cost < costs[child]:
                # either a cheaper path than we previously found, or a node
                # we've not seen before
                costs[child] = child_cost
                open_list[child] = costs[child]

    # we never found a path to the goal
    raise ValueError(f"No path from {start} to {end}")


def part1():
    machines = load_input()
    # This is a graph shortest path problem - states are all the
    # numbers in range(2**num_lights), transitions are from state
    # S to state S^b for each button b, start state is 0 and
    # destination state is target

    min_total_presses = sum(cheapest_path(0, m.target, m.buttons) for m in machines)

    print(f"Part 1: {min_total_presses=}")


if __name__ == "__main__":
    part1()
