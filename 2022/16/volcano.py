import itertools
import re
import time
from functools import cache
from collections import namedtuple

import networkx as nx

line_re = re.compile(
    r"^Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? (.*)$"
)


def load_data():
    non_zero_valves = {}
    graph = nx.Graph()
    with open("input", "r") as f:
        for l in f:
            m = line_re.match(l.strip())
            src = m.group(1)
            flow = int(m.group(2))
            targets = m.group(3)
            if flow > 0:
                non_zero_valves[src] = flow
            for t in targets.split(","):
                graph.add_edge(src, t.strip())

    return non_zero_valves, graph


def part1():
    """
    My original approach to part 1 was top-down memoized recursion.
    """
    non_zero_valves, graph = load_data()

    distances = {}
    for src, dists in nx.all_pairs_shortest_path_length(graph):
        if src in non_zero_valves or src == "AA":
            distances[src] = {
                dest: dist for dest, dist in dists.items() if dest in non_zero_valves
            }

    @cache
    def best_total_flow(time_left: int, cur_node: str, already_open: frozenset[str]):
        dists_from_cur = distances[cur_node]
        possible_answers = set()
        for dest, dist in dists_from_cur.items():
            if dest in already_open:
                continue
            valve_flow = non_zero_valves[dest]
            time_to_open = dist + 1
            if time_to_open >= time_left:
                continue
            possible_answers.add(
                (time_left - time_to_open) * valve_flow
                + best_total_flow(
                    time_left - time_to_open, dest, already_open.union({dest})
                )
            )

        return max(possible_answers, default=0)

    start = time.perf_counter()
    total_flow = best_total_flow(30, "AA", frozenset())
    end = time.perf_counter()
    print(f"Part 1: max total flow: {total_flow} (found in {end - start} seconds)")


Task = namedtuple("Task", ["node", "open", "time_left", "total_flow"])


def part2():
    """
    For part 2 we need to know what would happen for *all* subsets of the possible
    valve activations, in order to pick the best combination between me and the
    elephant, so switched from a top-down depth first recursion to a breadth-first
    traversal, keeping track of the highest flow rate achievable by a route that
    opens just the subset of valves we have visited so far.  Once we know this for
    all possible subsets, then the final answer is the highest sum you get from any
    pair of *disjoint* subsets (since we can't both open the same valve).
    """
    non_zero_valves, graph = load_data()

    distances = {}
    for src, dists in nx.all_pairs_shortest_path_length(graph):
        if src in non_zero_valves or src == "AA":
            distances[src] = {
                dest: dist for dest, dist in dists.items() if dest in non_zero_valves
            }

    best_total_per_subset = {}
    tasks = [Task("AA", frozenset(), 26, 0)]
    while tasks:
        t = tasks.pop()
        dists_from_cur = distances[t.node]
        for dest, dist in dists_from_cur.items():
            if dest not in t.open and dist + 1 <= t.time_left:
                # how much time would be left after we move to dest and open the valve
                time_left_after_move = t.time_left - dist - 1
                # how much total flow would we have by the time limit if we were to
                # stop after this step and not open any more valves
                new_total_flow = (
                    t.total_flow + time_left_after_move * non_zero_valves[dest]
                )
                new_task = Task(
                    dest, t.open.union({dest}), time_left_after_move, new_total_flow
                )
                if new_task.total_flow > best_total_per_subset.get(new_task.open, 0):
                    best_total_per_subset[new_task.open] = new_task.total_flow
                tasks.append(new_task)

    # now we know the best totals we could achieve by opening any subset of the valves,
    # so consider all the ways we could divide the work up between two actors such that
    # all the valves are open by the end, and see which split gives the highest result
    best_total = 0
    best_split = None
    for s1, s2 in itertools.combinations(best_total_per_subset.keys(), 2):
        if s1 & s2:
            # not disjoint
            continue
        this_total = sum(best_total_per_subset.get(s, 0) for s in (s1, s2))
        if this_total > best_total:
            best_split = (s1, s2)
            best_total = this_total

    print(
        f"Part 1: best total for one person in 26 sec: {max(best_total_per_subset.values())}"
    )
    print(f"Part 2: best total flow: {best_total}, by splitting as {best_split}")


if __name__ == "__main__":
    part1()
    part2()
