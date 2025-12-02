def main():
    with open("input", "r") as f:
        actions = [(-1 if line[0] == "L" else 1) * int(line[1:]) for line in f]

    # part 1
    pos = 50
    zeros = 0
    for action in actions:
        pos = (pos + action) % 100
        if pos == 0:
            zeros += 1

    print(f"number of zeros (part 1): {zeros}")

    # part 2
    pos = 50
    zeros = 0
    for action in actions:
        # we pass-or-arrive-at zero once for every full turn of the dial
        full_turns = abs(action) // 100
        zeros += full_turns
        old_pos, pos = pos, (pos + action) % 100
        # we now have the final less-than-full-turn to account for, and this
        # may add one more zero crossing if the previous position was not
        # already zero (if we were at zero before then we can't hit it again
        # in less than a full revolution)
        if old_pos != 0:
            # we cross-or-hit zero in this final part-revolution if either
            # (a) we're moving right and finish at a lower number than we
            # started (which may be zero) or (b) we're moving left and we
            # finish either _at_ zero, or past zero and at a number higher
            # than where we started.
            if (action < 0 and (pos == 0 or pos > old_pos)) or (
                action > 0 and pos < old_pos
            ):
                zeros += 1

    print(f"number of times passing zero (part 2): {zeros}")


if __name__ == "__main__":
    main()
