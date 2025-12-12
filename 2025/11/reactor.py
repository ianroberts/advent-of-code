import itertools
from functools import cache

import networkx


def load_input():
    with open("input", "r") as f:
        lines = [l.strip().split(": ") for l in f]

    edges = [(l[0], t) for l in lines for t in l[1].split()]
    return edges, lines


def graph_to_dot(lines):
    """
    Convert the graph input format into a graphviz file suitable
    for rendering with ``dot``.
    """
    print("digraph {")
    for src, targets in lines:
        # Highlight the critical nodes
        if src == "you":
            print(f'  {src} [fillcolor="blue", style=filled]')
        elif src == "fft":
            print(f'  {src} [fillcolor="red", style=filled]')
        elif src == "dac":
            print(f'  {src} [fillcolor="green", style=filled]')
        print(f"  {src} -> " + "{" + targets + "}")

    print("}")


def count_routes(edges, start, end, via=()):
    g = networkx.DiGraph(edges)

    @cache
    def routes(a, b):
        """
        Memoized recursive function to calculate the number of routes
        from a to b as follows:

          - there is 1 route to b from itself
          - otherwise the number of routes to b from a is the sum of
            the number of routes to b from each successor of a - this
            will be zero if a does not have any successors at all, or
            if none of its successors are able to reach node b.

        """
        if a == b:
            return 1
        return sum(routes(succ, b) for succ in g.successors(a))

    # If we want all routes from start to end via each of the via points
    # in order, then that is the number of routes from start to the first
    # via point, times the number from via[0] to via[1], etc. times the
    # number from via[-1] to end.  Use the handy itertools.pairwise,
    # which turns a sequence of N items ABCDEFG into a sequence of N-1
    # pairs AB BC CD DE EF FG
    product = 1
    for n1, n2 in itertools.pairwise([start, *via, end]):
        product *= routes(n1, n2)

    print(product)


if __name__ == "__main__":
    graph_edges, input_lines = load_input()
    # visualise the graph so we can work out whether our input has
    # fft before dac or dac before fft
    # graph_to_dot(input_lines)

    # Part 1
    count_routes(graph_edges, "you", "out")
    # Part 2 - in my input fft is before dac in all possible paths
    count_routes(graph_edges, "svr", "out", ("fft", "dac"))
