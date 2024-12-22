#
# This was my second attempt - instead of starting from the human and
# working forwards, start from the goal and work back.  If we want the
# final robot to press these buttons, what directions does its controller
# need to press, then what directions does *its* controller have to press,
# etc. etc.
#

import itertools
from functools import cache

from aoc_common.grid import Cell

DIRECTION_BUTTONS = "^A<v>"

# Button positions on the two keypads - to simplify the logic for computing paths,
# the blank space is at Cell(0, 0) in both cases, meaning that for the numpad the
# rows count upwards (positive numbers) and for the directional pad the second row
# is -1
NUMPAD_POSITIONS = dict(
    (
        ("A", Cell(0, 2)),
        ("0", Cell(0, 1)),
    )
    + tuple((str(n + 1), Cell(n // 3 + 1, n % 3)) for n in range(9))
)

DIRPAD_POSITIONS = {
    "A": Cell(0, 2),
    "^": Cell(0, 1),
    "<": Cell(-1, 0),
    "v": Cell(-1, 1),
    ">": Cell(-1, 2),
}


def keypad_paths(
    last_button: str, next_button: str, positions: dict[str, Cell]
) -> tuple[str, ...]:
    """
    For a given set of keypad positions, if the robot controlled by this keypad has
    just pressed the ``last_button`` and I want it to press the ``next_button`` next, what
    possible sequences of buttons on this directional keypad need to be pressed to
    achieve that?  We only consider routes with at most one "corner", i.e. always move
    as far as needed on one axis before moving on the other.  When the keypad is being
    operated by a robot, any zigzag path will be more expensive than one with a single
    turn, since pressing the same button repeatedly requires no movements by the
    controlling robot.

    :return: a tuple of either one or two button sequences, ending with "A", that
             would cause a robot currently pointing at ``last_button`` to move to
             (if necessary) and then press the ``next_button``.
    """
    last_pos = positions[last_button]
    next_pos = positions[next_button]

    # An appropriate number of moves up or down
    vert = ("^" if next_pos.row > last_pos.row else "v") * abs(
        next_pos.row - last_pos.row
    )
    # An appropriate number of moves right or left
    horz = (">" if next_pos.col > last_pos.col else "<") * abs(
        next_pos.col - last_pos.col
    )

    if last_pos.col == 0 and next_pos.row == 0:
        # to avoid the blank space we *must* go across first, then up/down
        return (f"{horz}{vert}A",)

    if last_pos.row == 0 and next_pos.col == 0:
        # to avoid the blank space we *must* go up/down first, then across
        return (f"{vert}{horz}A",)

    # else, if we have to move both horizontally and vertically then we coul
    # pick either way first
    if horz and vert:
        return f"{horz}{vert}A", f"{vert}{horz}A"

    # else we only have to move on one axis (the other one is the empty string)
    return (f"{horz}{vert}A",)


# Memoized versions of keypad_paths for the two keypads


@cache
def numpad_paths(last_button: str, next_button: str) -> tuple[str, ...]:
    return keypad_paths(last_button, next_button, NUMPAD_POSITIONS)


@cache
def dirpad_paths(last_button: str, next_button: str) -> tuple[str, ...]:
    return keypad_paths(last_button, next_button, DIRPAD_POSITIONS)


def load_data():
    with open("input", "r") as f:
        return [l.strip() for l in f]


@cache
def dir_move_cost(from_key: str, to_key: str, num_robots: int) -> int:
    """
    Given a chain of ``num_robots`` robots pressing directional keypads, the
    last of which is currently pointing at ``from_key``, compute the minimum number
    of keypresses on the keypad controlling the *first* robot in the chain that
    will cause the *last* robot in that chain to move to (if necessary) and press
    ``to_key``.
    """
    paths = dirpad_paths(from_key, to_key)
    if num_robots == 1:
        # The first robot *is* the last robot, so the minimum number of keypresses
        # to make that robot press to_key is simply the length of the shortest
        # path
        return min(len(path) for path in paths)

    # Otherwise, we need to make the second-to-last robot follow a path that would
    # move the last one from from_key to to_key, i.e. the minimum number of presses
    # that would make a chain one shorter move along all the steps of that path.
    # We return whichever of our candidate paths is cheapest.
    return min(
        sum(
            dir_move_cost(a, b, num_robots - 1)
            for a, b in itertools.pairwise("A" + path)
        )
        for path in paths
    )


@cache
def number_move_cost(from_key: str, to_key: str, num_robots: int) -> int:
    """
    Given a chain of ``num_robots`` robots pressing directional keypads, the
    last of which controls a robot pressing a numeric keypad, and that final
    robot is currently pointing at ``from_key``, compute the minimum number
    of keypresses on the keypad controlling the *first* robot in the chain that
    will cause the *final* robot to move to (if necessary) and press ``to_key``.

    This is simply the cheapest way to make the final robot in the directional
    chain make a sequence of directional presses that would move the number
    robot from ``from_key`` to ``to_key``
    """
    paths = numpad_paths(from_key, to_key)
    return min(
        sum(dir_move_cost(a, b, num_robots) for a, b in itertools.pairwise("A" + path))
        for path in paths
    )


def cost(num_robots: int):
    codes = load_data()

    total_presses = 0
    total_cost = 0
    for code in codes:
        this_code_cost = sum(
            number_move_cost(a, b, num_robots)
            for a, b in itertools.pairwise("A" + code)
        )
        total_presses += this_code_cost
        total_cost += int(code[:3]) * this_code_cost

    print(f"minimum number of button presses to open door: {total_presses}")
    print(f"Total complexity: {total_cost}")


if __name__ == "__main__":
    # part 1
    cost(2)
    # part 2
    cost(25)
