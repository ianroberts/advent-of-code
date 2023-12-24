

# If hailstone S is at (x0 y0 z0) at time t=0 and travelling (dx dy dz) per unit time
# (in the provided data all dx, dy and dz are non-zero) then
#
# x = x0 + t*dx --> t = (x-x0)/dx
# y = y0 + t*dy --> t = (y-y0)/dy
#
# subtract second equation from first
#
# ((x-x0)dy - (y-y0)dx) / (dy*dx) = 0
#                        (x-x0)dy = (y-y0)dx
#                     (x-x0)dy/dx = (y-y0)
#                               y = y0 + (x-x0)dy/dx
#
# For a target area in the range from A to B inclusive, we can determine whether it hits
# the target area at all by first solving for t1 when x=A and t2 when x=B, and similarly
# t3 when y=A and t4 when y=B.
#
# If the ranges [min(t1,t2), max(t1,t2)] and [min(t3,t4), max(t3,t4)] overlap then S is,
# was, or will be in the target area at some time.  Trim off any part of this overlap
# where t < 0 to get the time that S will be inside the target area in the future.  And
# finally use the original equations to find the subset C of the whole target area that S
# will traverse.  This box may be empty.
#
# Now to determine whether two 2d paths intersect, take the intersection of their "crossing
# boxes" C and compute y for each path at the left and right x values of this intersection.
# If y11-y12 and y21-y22 have opposite signs then the paths will cross, if they
# have the same sign then the paths won't cross.

from collections import namedtuple


class Particle(namedtuple("Particle", ["x0", "y0", "z0", "dx", "dy", "dz"])):
    def time_within_2d(self, coord_min, coord_max):
        x_entry = max(0, (coord_min - self.x0) / self.dx)
        x_exit = max(0, (coord_max - self.x0) / self.dx)
        if x_exit < x_entry:
            x_entry, x_exit = x_exit, x_entry

        y_entry = max(0, (coord_min - self.y0) / self.dy)
        y_exit = max(0, (coord_max - self.y0) / self.dy)
        if y_exit < y_entry:
            y_entry, y_exit = y_exit, y_entry

        if x_exit < y_entry or y_exit < x_entry:
            # never in the target box
            return None, None

        # otherwise, it was in the box between the latest entry and earliest exit times
        return max(x_entry, y_entry), min(x_exit, y_exit)

    def box_crossing_2d(self, coord_min, coord_max):
        entry, exit = self.time_within_2d(coord_min, coord_max)
        if entry is None or exit is None:
            return None, None

        x_entry = self.x0 + entry*self.dx
        x_exit = self.x0 + exit*self.dx
        y_entry = self.y0 + entry*self.dy
        y_exit = self.y0 + exit*self.dy

        if x_exit < x_entry:
            x_entry, x_exit, y_entry, y_exit = x_exit, x_entry, y_exit, y_entry

        return (x_entry, y_entry), (x_exit, y_exit)

    def y_at_x(self, x):
        return self.y0 + (x - self.x0) * self.dy / self.dx

    def intersects_2d(self, other, coord_min, coord_max):
        my_box_left, my_box_right = self.box_crossing_2d(coord_min, coord_max)
        other_box_left, other_box_right = other.box_crossing_2d(coord_min, coord_max)
        if my_box_left is None or other_box_left is None:
            # One or both particles never enters the box
            return False

        intersection_left = max(my_box_left[0], other_box_left[0])
        intersection_right = min(my_box_right[0], other_box_right[0])
        if intersection_right < intersection_left:
            # no overlap between the boxes
            return False

        ydiff_left = (
                self.y_at_x(intersection_left)
                - other.y_at_x(intersection_left)
        )
        ydiff_right = (
                self.y_at_x(intersection_right)
                - other.y_at_x(intersection_right)
        )

        # There's a collision if the left and right differences have opposite sign
        # (counting zero as positive)
        if (ydiff_left < 0) != (ydiff_right < 0):
            print(f"crossing within X range {intersection_left} to {intersection_right}")
            print(f"Y values left: me={self.y_at_x(intersection_left)} other={other.y_at_x(intersection_left)}")
            print(f"Y values at right: me={self.y_at_x(intersection_right)} other={other.y_at_x(intersection_right)}")
            return True
        return False


def parse_input():
    particles = []
    with open("input", "r") as f:
        for line in f:
            particles.append(Particle(*(int(x) for x in line.strip().replace(',', '').replace('@', '').split())))

    return particles


def intersecting_traces(coord_min, coord_max):
    particles = parse_input()
    crossing = 0
    for i in range(1, len(particles)):
        for j in range(i):
            if particles[i].intersects_2d(particles[j], coord_min, coord_max):
                crossing += 1

    return crossing


if __name__ == "__main__":
    print(f"{intersecting_traces(200000000000000, 400000000000000)} intersecting traces")
    # print(f"{intersecting_traces(7, 27)} intersecting traces")
