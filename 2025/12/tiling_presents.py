import re

region_re = re.compile(r"(\d+)x(\d+): (.*)")

def load_input():
    shapes: list[list[str]] = []
    regions = []
    with open("input", "r") as f:
        for line in f:
            line = line.strip()
            if line.endswith(":"):
                cur_shape = []
                while (l := f.readline().strip()):
                    cur_shape.append(l)
                shapes.append(cur_shape)
            else:
                w, h, counts = region_re.match(line).groups()
                regions.append((int(w), int(h), tuple(int(c) for c in counts.split())))

    return shapes, regions


def main():
    shapes, regions = load_input()
    covered_areas = [sum(l.count("#") for l in s) for s in shapes]

    fitting_regions = 0
    for n, (w, h, counts) in enumerate(regions):
        # Simple cases first:
        #
        # All the shapes are 3x3, so if the region has at least as many 3x3 squares
        # within it as there are total presents, it's trivially possible to fit
        if (w // 3) * (h // 3) >= sum(counts):
            fitting_regions += 1
            continue

        # if the total number of squares in the region is less than the total
        # area covered by the presents, then there's no way this example will
        # fit
        if sum(area * num for area, num in zip(covered_areas, counts)) >= w * h:
            continue

        print(f"Line {n} cannot be solved by the tests so far")

        # Next I was going to try combinations, like in my input two 1s, two 2s,
        # or a 1 and a 2 together can fit into a 3x4 region, two 3s will fit into
        # a 4x4, one 0 and one 4 can fit into 3x5, etc. etc.  But I tried
        # submitting the trivial answer first and it said that one was right...

    print(fitting_regions)


if __name__ == "__main__":
    main()