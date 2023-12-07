from bisect import bisect_left


def build_tree():
    # initial state = just the root directory with zero size
    tree = {("/",): 0}
    cwd = ("/",)

    with open("input", "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("$ cd "):
                newdir = line[5:]
                if newdir == "/":
                    cwd = ("/",)
                elif newdir == "..":
                    cwd = cwd[0:-1]
                else:
                    cwd = cwd + (newdir,)
            elif line.startswith("dir "):
                # directory entry
                tree[cwd + (line[4:],)] = 0
            elif not line.startswith("$"):
                # file entry
                size, name = line.split(maxsplit=1)
                size = int(size)
                # add the size to all directories up the tree from the current one
                for i in range(len(cwd)):
                    tree[cwd[0:i+1]] += size

    return tree


if __name__ == "__main__":
    tree = build_tree()
    total_under_100k = sum(v for v in tree.values() if v <= 100_000)
    print(f"Total size of dirs under 100k: {total_under_100k}")

    available_space = 70000000 - tree[("/",)]
    print(f"Current available space: {available_space}")
    need_to_free = 30000000 - available_space
    print(f"Need to free up {need_to_free}")
    dir_sizes = sorted(tree.values())
    print(f"Smallest directory size >= {need_to_free} == {dir_sizes[bisect_left(dir_sizes, need_to_free)]}")
