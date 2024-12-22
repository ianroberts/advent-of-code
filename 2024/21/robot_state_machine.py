#
# This was my first attempt at an algorithm that treats the problem
# as finite state machine and attempts to find a series of shortest
# paths through the state graph.  It worked for part 1 but the state
# graph was far too large to be tractable for part 2.
#

import itertools
from typing import NamedTuple
from functools import cache

from aoc_common.heapdict import heapdict

DIRECTION_BUTTONS = "A^<v>"
# DIRECTION_MOVES[from][press] is the button you end up on if you were on "from" and
# your controller presses "press"
DIRECTION_MOVES = {
    "A": {"<": "^", "v": ">"},
    "^": {">": "A", "v": "v"},
    "<": {">": "v"},
    "v": {"<": "<", "^": "^", ">": ">"},
    ">": {"<": "v", "^": "A"},
}

NUMBER_MOVES = {
    "A": {"^": "3", "<": "0"},
    "0": {">": "A", "^": "2"},
    "1": {">": "2", "^": "4"},
    "2": {"<": "1", "^": "5", "v": "0", ">": "3"},
    "3": {"<": "2", "^": "6", "v": "A"},
    "4": {">": "5", "v": "1", "^": "7"},
    "5": {"<": "4", ">": "6", "v": "2", "^": "8"},
    "6": {"<": "5", "v": "3", "^": "9"},
    "7": {"v": "4", ">": "8"},
    "8": {"<": "7", "v": "5", ">": "9"},
    "9": {"<": "8", "v": "6"},
}


class State(NamedTuple):
    arrows: tuple[str, ...]
    numbers: str


@cache
def next_state(state: State, button: str):
    if button == "A":
        # A doesn't move anything on this layer but it might advance the next layer(s)
        if len(state.arrows):
            advanced = next_state(
                State(state.arrows[1:], state.numbers), state.arrows[0]
            )
            if advanced is None:
                # Pressing this button would move one of the robots off the keypad
                return None
            return State((state.arrows[0], *advanced.arrows), advanced.numbers)

        # No arrow layers remaining, nothing changes
        return state

    if len(state.arrows):
        if button not in DIRECTION_MOVES[state.arrows[0]]:
            # this would move us off the keypad
            return None

        # make the move
        return State(
            (DIRECTION_MOVES[state.arrows[0]][button], *state.arrows[1:]), state.numbers
        )

    # no arrows - we're in the numbers layer
    if button not in NUMBER_MOVES[state.numbers]:
        # This would move us off the keypad
        return None

    return State(state.arrows, NUMBER_MOVES[state.numbers][button])


def load_data():
    with open("input", "r") as f:
        return [l.strip() for l in f]


def cheapest_path(start, end):
    # Dijkstra to find the shortest path from start to end

    # Use a heapdict for the unvisited list so the next node to be processed
    # is always the one with the lowest cost path from the start
    open_list = heapdict()
    # closed_list is the set of nodes we have completely visited
    closed_list: set[State] = set()
    # costs is the total cost of the cheapest path so far found to each node
    # (including the fully visited ones)
    costs: dict[State, int] = {}
    pred = {}

    # Initial conditions - we're starting from the start node, and its
    # distance from the start node is (obviously) zero
    open_list[start] = 0
    costs[start] = 0

    while len(open_list):
        node, dist_node = open_list.popitem()
        closed_list.add(node)

        if node == end:
            # we have reached the goal
            presses = []
            while node != start:
                presses.append(pred[node][0])
                node = pred[node][1]

            path = "".join(reversed(presses))
            print(f"Path from {start} to {end}: {path}")
            return path

        for button in DIRECTION_BUTTONS:
            child = next_state(node, button)
            if child is None or child in closed_list:
                continue
            child_cost = costs[node] + 1
            if child not in costs or child_cost < costs[child]:
                # either a cheaper path than we previously found, or a node
                # we've not seen before
                costs[child] = child_cost
                pred[child] = (button, node)
                open_list[child] = costs[child]

    # we never found a path to the goal
    raise ValueError(f"No path from {start} to {end}")


def cost(robots: int):
    codes = load_data()

    total_presses = 0
    total_cost = 0
    for code in codes:
        required_states = [State(tuple("A" * robots), "A")]
        for ch in code:
            required_states.append(State(tuple("A" * robots), ch))

        for state1, state2 in itertools.pairwise(required_states):
            code_presses = (
                len(cheapest_path(state1, state2)) + 1
            )  # +1 for pressing the final A
            total_presses += code_presses
            total_cost += code_presses * int(code[:3])

    print(f"minimum number of button presses to open door: {total_presses}")
    print(f"Total complexity: {total_cost}")


if __name__ == "__main__":
    # Part 1
    cost(2)
    # Part 2 - this algorithm is intractable
    # cost(25)
