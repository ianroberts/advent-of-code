from itertools import chain


def parse_input():
    with open("input", "r") as f:
        # Represent each tree as 2^height, i.e. exactly one bit set
        return [[1 << ord(c)-48 for c in line.strip()] for line in f]


def update_visibility(r, get_tree, set_viz):
    bitmap = 0
    for i in r:
        val = get_tree(i)
        if val > bitmap:
            set_viz(i, True)
        bitmap |= val


def visible_trees():
    trees = parse_input()
    visibility = [[False for _ in row] for row in trees]

    # looking across the rows
    for i, (row_trees, row_viz) in enumerate(zip(trees, visibility)):
        # left to right
        update_visibility(range(len(row_trees)), row_trees.__getitem__, row_viz.__setitem__)
        # right to left
        update_visibility(range(len(row_trees) - 1, -1, -1), row_trees.__getitem__, row_viz.__setitem__)

    # looking up and down the columns
    for j in range(len(trees[0])):
        def get_tree(i):
            return trees[i][j]

        def set_viz(i, val):
            visibility[i][j] = val

        # top to bottom
        update_visibility(range(len(trees)), get_tree, set_viz)
        # bottom to top
        update_visibility(range(len(trees) - 1, -1, -1), get_tree, set_viz)

    # pretty picture
    num_visible = 0
    for row in visibility:
        num_visible += row.count(True)
        print("".join('#' if t else "." for t in row))

    return num_visible


def update_scenic(r, get_tree, set_scenic):
    for x, i in enumerate(r):
        tree_i = get_tree(i)
        view = 0
        for j in r[x+1:]:
            view += 1
            if get_tree(j) >= tree_i:
                break
        set_scenic(i, view)


def scenic_scores():
    trees = parse_input()
    scenic_score = [[1 for _ in row] for row in trees]
    scenic_score[0] = [0 for _ in range(len(scenic_score[0]))]
    scenic_score[-1] = [0 for _ in range(len(scenic_score[-1]))]
    for row in scenic_score:
        row[0] = 0
        row[-1] = 0

    # looking across the rows
    for i, (row_trees, row_scenic) in enumerate(zip(trees, scenic_score)):
        def set_scenic(j, val):
            row_scenic[j] *= val
        update_scenic(range(len(row_trees)), row_trees.__getitem__, set_scenic)
        update_scenic(range(len(row_trees) - 1, -1, -1), row_trees.__getitem__, set_scenic)

    # looking along the columns
    for j in range(len(trees[0])):
        def get_tree(i):
            return trees[i][j]

        def set_scenic_col(i, val):
            scenic_score[i][j] *= val

        # top to bottom
        update_scenic(range(len(trees)), get_tree, set_scenic_col)
        # bottom to top
        update_scenic(range(len(trees) - 1, -1, -1), get_tree, set_scenic_col)

    print(scenic_score)

    return max(chain(*scenic_score))


if __name__ == "__main__":
    print(f"Total number of visible trees: {visible_trees()}")
    print(f"Maximum scenic score: {scenic_scores()}")