import functools
import operator
from collections import namedtuple

from bitarray import frozenbitarray
from bitarray.util import zeros

Cell = namedtuple("Cell", ["x", "y", "z"])
ZERO_FP = frozenbitarray(zeros(100))
BRICKS = None
LAYERS = []


def print_fp(footprint, caption):
    print(caption)
    for i in range(10):
        print(footprint[10*i:10*(i+1)])


class Brick:
    def __init__(self, end_a: Cell, end_b: Cell):
        self.a = end_a
        self.b = end_b
        xs = range(end_a.x, end_b.x+1)
        ys = range(end_a.y, end_b.y+1)
        footprint = zeros(100)
        for y in ys:
            for x in xs:
                footprint[10*y+x] = 1
        self.footprint = frozenbitarray(footprint)

        self.bottom = end_a.z
        self.top = end_b.z

    def __repr__(self):
        return f"{self.a}~{self.b}"

    def footprint_at(self, z):
        if self.bottom <= z <= self.top:
            return self.footprint
        else:
            return ZERO_FP


def parse_input():
    global BRICKS
    global LAYERS
    BRICKS = []
    with open("input", "r") as f:
        for line in f:
            ends = line.split("~", 1)
            end_a = Cell(*(int(c) for c in ends[0].split(",")))
            end_b = Cell(*(int(c) for c in ends[1].split(",")))
            BRICKS.append(Brick(end_a, end_b))

    # Sort BRICKS in order of their bottom Z co-ordinate, lowest first
    BRICKS.sort(key=operator.attrgetter("bottom"))

    # index BRICKS by layer - make a list of LAYERS where each layer is the list of
    # BRICKS that have one or more of their cubes somewhere in that layer
    LAYERS = [[] for z in range(max(b.top for b in BRICKS)+1)]
    for b in BRICKS:
        for layer in LAYERS[b.bottom:b.top+1]:
            layer.append(b)

    settle(BRICKS, LAYERS)


def layer_footprint(layer):
    return functools.reduce(operator.or_, (b.footprint for b in layer), ZERO_FP)


def settle(bricks, layers):
    for b in bricks:
        bottom = b.bottom
        top = b.top
        brick_footprint = b.footprint
        while bottom > 0 and not (brick_footprint & layer_footprint(layers[bottom-1])).any():
            bottom -= 1
            top -= 1

        if bottom < b.bottom:
            # need to move this brick down to its new bottom layer:
            for layer in layers[max(b.bottom, top+1):b.top+1]:
                layer.remove(b)
            for layer in layers[bottom:min(b.bottom, top+1)]:
                layer.append(b)

            b.bottom, b.top = bottom, top

    # done all the bricks, now re-sort the bricks list by their new bottom Z coord
    bricks.sort(key=operator.attrgetter("bottom"))

    # prune empty top layers
    i = len(layers) - 1
    while len(layers[i]) == 0:
        layers.pop(i)
        i -= 1


def count_disintegrable():
    disintegrable = 0
    # Consider each layer in turn.  For each brick B1 whose top end is in that layer, compute the
    # layer's footprint with (L+) and without (L-) the given brick.  B1 is disintegrable if there
    # is no brick B2 in the layer above whose footprint overlaps L+ but not L-
    for i in range(len(LAYERS)-1):
        layer_i_fp = layer_footprint(LAYERS[i])
        for b in LAYERS[i]:
            if b.top == i:
                footprint_without_b = layer_i_fp & ~b.footprint
                for b2 in LAYERS[i+1]:
                    if not (b2.footprint & footprint_without_b).any():
                        # we've found a brick above for which b is the sole support
                        break
                else:
                    # if we get to here, b is not the sole support for anything
                    disintegrable += 1

    # also any blocks in the topmost layer are automatically disintegrable without disturbing
    # anything else
    disintegrable += len(LAYERS[-1])

    return disintegrable


def sole_support(layernum, support):
    """
    Return the number of bricks whose bottom end is at or above layernum and which are only supported
    by the given footprint in the layer below layernum (or by any of those bricks recursively)
    :param layernum: the layer number
    :param support: current supporting footprint from the next layer down
    """
    if layernum >= len(LAYERS):
        return 0

    brick_count = 0
    # start with the full footprint of the next layer down
    supporting_layer_fp = layer_footprint(LAYERS[layernum-1])
    # remove the specified supporting points
    layer_without_support = supporting_layer_fp & ~support

    next_layer_support = ZERO_FP
    for b in LAYERS[layernum]:
        if not (b.footprint & layer_without_support).any():
            # if support were removed, this brick b would be unsupported, therefore anything above it
            # that is solely supported by b would also end up unsupported when b falls
            next_layer_support = next_layer_support | b.footprint
            if b.bottom == layernum:
                # however it may be the case that the reason b's footprint is considered "unsupported"
                # is because b is a z-oriented brick that protrudes into this layer from the one below.
                # In that case b will already have been counted when considering the lower layer, and
                # we don't want to count it again here - brick_count should only include unsupported
                # bricks whose bottom end is in the current layernum
                brick_count += 1

    if next_layer_support.any():
        # at least one brick in this layer had its sole support from the previous footprint
        return brick_count + sole_support(layernum + 1, next_layer_support)
    else:
        # no unsupported bricks at this layer, so we know there can be no further unsupported bricks
        # in the higher layers either.
        return 0


if __name__ == "__main__":
    parse_input()

    print(f"Number of independently disintegrable bricks: {count_disintegrable()}")

    total_to_move = 0
    for b in BRICKS:
        supported_by_b = sole_support(b.bottom+1, b.footprint)
        total_to_move += supported_by_b
        # print(f"{supported_by_b} bricks would fall if {b} were removed")

    print("Sum over all bricks of the number of other bricks that would fall if that brick were removed:",
          total_to_move)