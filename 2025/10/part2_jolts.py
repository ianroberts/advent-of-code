import re
from collections import namedtuple
import numpy as np
from scipy.optimize import milp

LINE_PATTERN = re.compile(r"^\[(?P<target>[.#]+)] (?P<buttons>\(.*\)) \{(?P<jolts>.*)}")
BUTTON_PATTERN = re.compile(r"\((.*?)\)")

Machine = namedtuple("Machine", ["buttons", "jolts"])

def load_input():
    with open("input", "r") as f:
        machines = []
        for line in f:
            line = line.strip()
            m = LINE_PATTERN.match(line)
            if not m:
                raise ValueError(f"Invalid input line: {line}")

            # ignore the targets for part 2

            # represent each button as the tuple of counters that it increments
            buttons = []
            for b in BUTTON_PATTERN.findall(m.group("buttons")):
                buttons.append(tuple(int(l) for l in b.split(",")))

            # target jolts per counter
            jolts = tuple(int(j) for j in m.group("jolts").split(","))

            machines.append(Machine(buttons=buttons, jolts=jolts))

    return machines

def part2():
    machines = load_input()

    # Since each button increments one or more counters by exactly 1,
    # we know that for each counter, the *sum* of the number of presses
    # across all the buttons that could increment that counter must be
    # equal to the target value for that counter.  For a set of b buttons
    # and n counters this gives us a system of n simultaneous linear
    # equations in b unknowns.  When we constrain the coefficients to
    # be non-negative integers, this system will have a finite number
    # of possible solutions (bounded by the sum of all the jolt targets),
    # we want (one of) the ones with the smallest sum of the coefficient
    # values.
    #
    # This is an integer linear programming problem: minimise (c.T) @ x
    # where x is the vector of b unknowns and c is a same-length column
    # vector of all ones, such that the n equations all hold and the x
    # elements are all integers >= 0.  And scipy has a function to solve
    # exactly those kinds of problems...

    total_presses = 0
    for i, machine in enumerate(machines):
        c = np.ones((len(machine.buttons),))
        integrality = c  # all button variables must be integers
        # constraint array is one row per counter with as many columns
        # as there are buttons, the value in each column is 1 if that
        # button can increment that counter, 0 if not.
        A = np.array([[1 if n in but else 0 for but in machine.buttons] for n in range(len(machine.jolts))])
        # upper and lower bound vectors are the same, namely the target
        # number of jolts per counter
        ub = lb = np.array(machine.jolts)

        # No need to specify upper and lower bounds on the x vector as the
        # defaults are correct for what we need (lower bound 0, no upper bound)
        result = milp(c, integrality=integrality, constraints=(A, lb, ub))
        presses = int(result.fun)  # value of c.T @ x at the minimum

        print(f"Machine {i} presses: {presses}")
        total_presses += presses

    print(f"{total_presses=}")


if __name__ == "__main__":
    part2()