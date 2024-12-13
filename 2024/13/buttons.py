from collections import namedtuple
import re

COORDINATE = re.compile("[=+](\d+)")

Vector = namedtuple("Vector", ["x", "y"])
Machine = namedtuple("Machine", ["a", "b", "prize"])

def to_vector(line):
    return Vector(*(int(m.group(1)) for m in COORDINATE.finditer(line)))


def load_data():
    with open("input", "r") as f:
        machines = []
        while a := f.readline():
            a = a.strip()
            b = f.readline().strip()
            prize = f.readline().strip()
            gap = f.readline()

            machines.append(Machine(to_vector(a), to_vector(b), to_vector(prize)))

    return machines


# Verify none of the machines have their a/b vectors parallel
# for i, m in enumerate(load_data()):
#     if (m.a.x >= m.a.y) == (m.b.x >= m.b.y):
#         print(f"{i=} {m=}, a gradient {m.a.y / m.a.x}, b gradient {m.b.y / m.b.x}")

# This means there is at most one way to win on each machine - there is a unique solution
# to the simultaneous equations in A and B:
#
# A(a.x) + B(b.x) = (prize.x)
# A(a.y) + B(b.y) = (prize.y)
#
# A = (prize.x - B(b.x)) / (a.x)
#
# so
#
# ((prize.x - B(b.x))/(a.x))(a.y) + B(b.y) = (prize.y)
#  (prize.x - B(b.x))/(a.x) = (prize.y - B(b.y))/(a.y)
#  (a.y)(prize.x) - (a.y)(b.x)B = (a.x)(prize.y) - (b.y)(a.x)B
# B((b.y)(a.x) - (a.y)(b.x)) = (a.x)(prize.y) - (a.y)(prize.x)
# B = ((a.x)(prize.y) - (a.y)(prize.x))/((b.y)(a.x) - (a.y)(b.x))
#
# and substitute in to find A - game is winnable if and only if A and B are
# both integers

def winnable_games(prize_delta=0):
    machines = load_data()
    cost = 0
    for i, (a, b, prize) in enumerate(machines):
        if prize_delta > 0:
            prize = Vector(prize.x + prize_delta, prize.y + prize_delta)
        big_b, remainder = divmod((a.x) * (prize.y) - (a.y) * (prize.x), (b.y) * (a.x) - (a.y) * (b.x))
        if remainder != 0:
            continue

        big_a, remainder = divmod(prize.x - big_b * b.x, a.x)
        if remainder != 0:
            continue

        m_cost = 3 * big_a + big_b
        # print(f"Machine {i} is winnable with {big_a} As and {big_b} Bs, costing {m_cost}")
        cost += m_cost

    print(f"Total cost {cost}")


if __name__ == "__main__":
    winnable_games(0)
    winnable_games(10000000000000)