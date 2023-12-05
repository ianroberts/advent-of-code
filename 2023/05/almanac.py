import functools
from bisect import bisect_right


class MappingRange:
    def __init__(self, line):
        self.dest_start, src_start, src_len = (int(n) for n in line.split())
        self.src_range = range(src_start, src_start+src_len)

    def __getitem__(self, item):
        if item in self.src_range:
            return self.dest_start + item - self.src_range.start
        else:
            raise KeyError(item)

    def __contains__(self, item):
        return item in self.src_range

    def __len__(self):
        return len(self.src_range)

    def __repr__(self):
        return f"{self.src_range!r} -> {self.dest_start}"

    @property
    def start(self):
        return self.src_range.start

    @property
    def stop(self):
        return self.src_range.stop


class AlmanacMapping:
    def __init__(self, block_title, lines):
        self.ranges = []
        self.title = block_title.strip()
        for line in lines:
            line = line.strip()
            if not line:
                break
            self.ranges.append(MappingRange(line))

        self.ranges.sort(key=lambda r: r.start)
        self.starts = [r.start for r in self.ranges]

    def __getitem__(self, item):
        candidate = bisect_right(self.starts, item) - 1
        if candidate >= 0 and item in self.ranges[candidate]:
            return self.ranges[candidate][item]
        else:
            # if not covered by any of the ranges then use identity mapping
            return item

    def __repr__(self):
        return f"{self.title} {self.ranges!r}"

    def map_range(self, r: range):
        """
        Compute the set of ranges denoting possible outputs from this mapping, if it were
        given inputs from a specified range.
        :param r: the input range
        :return: list of one or more ranges that this range transforms to via this mapping.
        It should always be the case that ``sum(len(out_r) for out_r in output) == len(r)``
        """
        mapped = []
        startpoint = 0
        while len(r) > 0:
            candidate = bisect_right(self.starts, r.start, startpoint) - 1
            if candidate < 0 or r.start not in self.ranges[candidate]:
                # r starts before/after/between our ranges ...
                if candidate+1 < len(self.ranges) and self.ranges[candidate + 1].start < r.stop:
                    # ... and ends within the next range
                    split_point = self.ranges[candidate+1].start
                else:
                    # ... and also ends without entering another range
                    split_point = r.stop
                mapped.append(range(r.start, split_point))
            else:
                # start of r is inside one of our ranges
                candidate_range = self.ranges[candidate]
                split_point = min((r.stop, candidate_range.stop))
                mapped.append(range(candidate_range[r.start], candidate_range[r.start] + split_point - r.start))

            # Replace r with the right hand split - this may be an empty range
            r = range(split_point, r.stop)
            # and we know that the new r can't touch the candidate we were previously looking at
            startpoint = candidate + 1

        return mapped


def parse_input():
    mappings = []
    with open("input", "r") as f:
        lines = iter(f)
        seeds_line = next(lines)
        _ = next(lines)  # Blank line following "seeds"
        for block_title in lines:
            # the first line of each block is the header
            almanac_mapping = AlmanacMapping(block_title, lines)
            mappings.append(almanac_mapping)
            # AlmanacMapping constructor will consume the lines of the block
            # and the following empty line separating this block from the next,
            # if we haven't already reached EOF

    seeds = [int(s) for s in seeds_line[7:].split()]  # chop off the header
    return seeds, mappings

def find_min_location():
    seeds, mappings = parse_input()
    return min(functools.reduce(lambda val, mapping: mapping[val], mappings, seed) for seed in seeds)


def find_min_from_ranges():
    seeds, mappings = parse_input()
    # turn each pair of seed numbers into the corresponding range
    itr = iter(seeds)
    ranges = [range(start, start+length) for start, length in zip(itr, itr)]
    ranges.sort(key=lambda r: r.start)

    # loop through the mappings, each time taking the list of ranges
    # produced by the previous stage and transforming them through this mapping
    for mapping in mappings:
        new_ranges = []
        for r in ranges:
            new_ranges.extend(mapping.map_range(r))
        ranges = new_ranges
        ranges.sort(key=lambda r: r.start)

        # amalgamate adjacent ranges - this isn't strictly necessary to the
        # algorithm, but it's nice to keep things tidy
        i = 0
        while i < len(ranges)-1:
            if ranges[i].stop == ranges[i+1].start:
                ranges[i:i+2] = [range(ranges[i].start, ranges[i+1].stop)]
            else:
                i += 1

        print(f"{mapping.title} {ranges!r}")

    # After all the transformations are done, what we care about is the
    # left edge of the leftmost final range
    return ranges[0].start




if __name__ == "__main__":
    print(f"closest location, treating seeds as single numbers: {find_min_location()}")
    print(f"closest location, treating seeds as ranges: {find_min_from_ranges()}")