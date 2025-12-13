import re
from operator import attrgetter

from aoc_common.grid import Cell


def load_data():
    regex = re.compile(r"Sensor at x=([0-9-]+), y=([0-9-]+): closest beacon is at x=([0-9-]+), y=([0-9-]+)")

    with open("input", "r") as f:
        # list of sensor/beacon tuples
        pairs = []
        for line in f:
            match = regex.search(line)
            if match:
                pairs.append((Cell(int(match.group(2)), int(match.group(1))), Cell(int(match.group(4)), int(match.group(3)))))

    return pairs


def cells_within_range(row: int, sensor: Cell, beacon: Cell) -> range | None:
    beacon_distance = abs(beacon.row - sensor.row) + abs(beacon.col - sensor.col)
    # number of rows above or below the sensor that we are asking about
    row_offset = abs(row - sensor.row)
    # number of columns to the left or right of the sensor that fall within the
    # beacon distance on the target row
    col_offset = beacon_distance - row_offset

    first_non_beacon = sensor.col - col_offset
    last_non_beacon = sensor.col + col_offset

    nbr = range(first_non_beacon, last_non_beacon + 1)
    if len(nbr) == 0:
        return None

    return nbr


def part1(pairs, row):
    ranges = []
    beacons = set()
    for sensor, beacon in pairs:
        r = cells_within_range(row, sensor, beacon)
        if r is not None:
            ranges.append(r)
        # also track any beacons that are actually in this row - a
        # cell that we know contains a beacon is by definition *not*
        # a "cell that cannot contain beacons"
        if beacon.row == row:
            beacons.add(beacon.col)

    print(f"{len(beacons)} cells in row {row} known to be beacons")

    ranges.sort(key=attrgetter("start"))
    print(ranges)

    cur_range = ranges[0]
    not_beacons = 0
    for r in ranges[1:]:
        if cur_range.stop < r.start:
            not_beacons += len(cur_range)
            print(f"no beacons in {cur_range}")
            cur_range = r
        elif cur_range.stop < r.stop:
            cur_range = range(cur_range.start, r.stop)
        # else r is wholly contained within cur_range

    if len(cur_range) > 0:
        not_beacons += len(cur_range)
        print(f"no beacons in {cur_range}")

    print(f"Number of cells in row {row} that cannot be beacons: {not_beacons - len(beacons)}")


def part2(pairs):
    for row in range(4000001):
        if row % 100000 == 0:
            print(f"{row}")
        ranges = []
        for sensor, beacon in pairs:
            r = cells_within_range(row, sensor, beacon)
            if r is not None:
                s = max(r.start, 0)
                e = min(r.stop, 4000001)
                if s < e:
                    ranges.append(r)

        ranges.sort(key=attrgetter("start"))
        # first edge case - if there's a gap at the start of this row
        # then that's the target
        if ranges[0].start > 0:
            return Cell(row, 0)
        cur_range = ranges[0]
        for r in ranges[1:]:
            if cur_range.stop < r.start:
                # we've found the only possible place for the missing beacon
                return Cell(row, cur_range.stop)
            elif cur_range.stop < r.stop:
                cur_range = range(cur_range.start, r.stop)
            # else r is wholly contained within cur_range

        # second edge case - if there's a gap at the end of this row
        # then that's the target
        if cur_range.stop < 4000001:
            return Cell(row, 400000)

    raise ValueError("No possible place for the missing beacon")


if __name__ == "__main__":
    sensors_and_beacons = load_data()
    part1(sensors_and_beacons, 2000000)
    target = part2(sensors_and_beacons)
    print(f"Tuning frequency: {target.col * 4000000 + target.row}")