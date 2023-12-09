from collections import namedtuple
Pos = namedtuple("Pos", ["x", "y"])

# direction label to move co-ordinates - X is left to right, Y is bottom to top
moves = {
    "L": Pos(-1, 0),
    "R": Pos(1, 0),
    "D": Pos(0, -1),
    "U": Pos(0, 1),
}


def add(p1, p2):
    return Pos(p1.x + p2.x, p1.y + p2.y)


def sub(p1, p2):
    return Pos(p1.x - p2.x, p1.y - p2.y)


def generate_steps():
    with open("input", "r") as f:
        for line in f:
            direction, distance = line.split()
            distance = int(distance)
            for _ in range(distance):
                yield moves[direction]


def chase_tail_simple():
    head_pos = Pos(0, 0)
    tail_pos = Pos(0, 0)
    visited = {tail_pos}
    for step in generate_steps():
        head_pos = add(head_pos, step)
        diff = sub(head_pos, tail_pos)
        # print(f"{step=}, new {head_pos=}, old {tail_pos=}, {diff=}")
        if abs(diff.x) == 2:
            tail_pos = add(tail_pos, Pos(diff.x//2, diff.y))
        elif abs(diff.y) == 2:
            tail_pos = add(tail_pos, Pos(diff.x, diff.y//2))
        # else tail doesn't need to move
        visited.add(tail_pos)

    # Final result - number of distinct locations where the tail has been
    return len(visited)


def chase_tail_general(num_knots):
    knots = [Pos(0, 0)] * num_knots
    visited = {knots[-1]}

    for step in generate_steps():
        # move the head as instructed
        knots[0] = add(knots[0], step)
        # now move each trailing knot relative to the previous one
        for i in range(1, len(knots)):
            diff = sub(knots[i-1], knots[i])
            if abs(diff.x) == 2 or abs(diff.y) == 2:
                if abs(diff.x) == 2:
                    diff = Pos(diff.x//2, diff.y)
                if abs(diff.y) == 2:
                    diff = Pos(diff.x, diff.y//2)
                # move this knot
                knots[i] = add(knots[i], diff)
            # else this knot doesn't need to move

        # all knots in their new positions, so record current position of the tail
        visited.add(knots[-1])

    # Final result - number of distinct locations where the tail has been
    return len(visited)



if __name__ == "__main__":
    print(f"2 knots - tail visited {chase_tail_simple()} locations")
    print(f"2 knots using general algorithm - tail visited {chase_tail_general(2)} locations")
    print(f"10 knots - tail visited {chase_tail_general(10)} locations")
