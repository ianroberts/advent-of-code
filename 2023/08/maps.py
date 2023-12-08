import math
from itertools import cycle

def parse_input():
    with open("input", "r") as f:
        itr = iter(f)
        instructions = next(itr).strip()
        network = {}
        for line in itr:
            line = line.strip()
            if not line:
                continue

            # ABC = (DEF, GHI)
            # 0123456789012345
            network[line[0:3]] = (line[7:10], line[12:15])

    return instructions, network


def follow_route_human():
    instructions, network = parse_input()
    steps = 0
    cur = "AAA"
    for step in cycle(instructions):
        steps += 1
        node = network[cur]
        if step == "L":
            cur = node[0]
        else:
            cur = node[1]

        if cur == "ZZZ":
            break

    return steps


def check_graph_structure():
    """
    Verifying exactly which Z nodes can be reached from which A nodes, and in how many steps
    """
    instructions, network = parse_input()
    cur_nodes = [k for k in network if k.endswith("A")]
    print(cur_nodes)

    for start in cur_nodes:
        print(f"Starting from {start}")
        cur = start
        steps = 0
        seen_zs = []
        zs_distances = [0]
        for step in cycle(instructions):
            steps += 1
            node = network[cur]
            if step == "L":
                cur = node[0]
            else:
                cur = node[1]

            if cur.endswith("Z"):
                print(f"  Reached {cur} in {steps} steps ({steps-zs_distances[-1]} since last Z)")
                zs_distances.append(steps)
                seen_zs.append(cur)
                if len(seen_zs) > 300:
                    break


def follow_route_ghost(instructions, network, start):
    steps = 0
    cur = start
    for step in cycle(instructions):
        steps += 1
        node = network[cur]
        if step == "L":
            cur = node[0]
        else:
            cur = node[1]

        if cur.endswith("Z"):
            break

    return steps


def find_all_zs():
    # so it seems this puzzle has been carefully engineered so that:
    # - each A links to exactly one Z
    # - if it takes N steps to get from the A to the Z and you continue following the instructions
    #   then you get back to the same Z again in another N steps, 2N steps, etc.
    # - I've checked this up to 300N which is beyond the length of the input instruction string, so
    #   it is genuinely the case for all time even if each time round the Z->Z cycle you're starting
    #   at a different place in the instruction sequence
    # Therefore the desired result is the LCM of all these Ns for each A node
    instructions, network = parse_input()
    start_nodes = [k for k in network if k.endswith("A")]
    return math.lcm(*(follow_route_ghost(instructions, network, n) for n in start_nodes))


if __name__ == "__main__":
    print(f"Human reached ZZZ in {follow_route_human()} steps")
    #check_graph_structure()
    #
    print(f"Ghost reached all-Zs in {find_all_zs()} steps")