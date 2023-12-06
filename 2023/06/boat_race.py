import math

def parse_input(ignore_spaces):
    with open("input", "r") as f:
        time_line, dist_line = (l.split()[1:] for l in f)
        if ignore_spaces:
            return [(int("".join(time_line)), int("".join(dist_line)))]
        else:
            return ((int(t), int(d)) for t, d in zip(time_line, dist_line))


def ways_to_win(ignore_spaces):
    product = 1
    for l, best_dist in parse_input(ignore_spaces):
        # in a race over l ms, holding the button for x ms
        # will result in the boat moving y = (l-x)*x mm.
        # Possible winning times are all the integer x values
        # for which
        #
        # -x^2 + lx - best_dist > 0
        # x^2 - lx + best_dist < 0
        #
        # solve for == 0, and since this is an inverted parabola
        # the winning times will be all x between the two real roots.
        # If there are 0 or 1 real root, or the two roots have no
        # integers strictly between them, then the record can't be
        # beaten
        radical = math.sqrt(l**2 - 4*best_dist)  # sqrt(b^2-4ac)
        left, right = ((l - radical)/2, (l + radical)/2)  # (b^2 +- radical)/2a
        print(f"roots: {left} {right}")
        winning_possibilities = range(int(left)+1, math.ceil(right))
        print(f"{len(winning_possibilities)} possibilities {winning_possibilities}")

        product *= len(winning_possibilities)

    return product


if __name__ == "__main__":
    print(f"Possible ways to win many races: {ways_to_win(False)}")
    print(f"Possible ways to win one race: {ways_to_win(True)}")
