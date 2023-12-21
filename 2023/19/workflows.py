from dataclasses import dataclass
from collections import namedtuple


# The overall approach is to "compile" the set of workflows into a binary decision tree.
# Each node in the tree is either a "Leaf" node that either accepts or rejects all input,
# or a "Branch" node that tests one of the four "xmas" variables against a threshold and
# chooses the left or right branch depending whether the value is < or >= the threshold.
# So a workflow step compiles to a Branch node as:
#
#               "v<val:target"                        "v>val:target"
#                  var: v                                var: v
#            threshold: val                        threshold: val+1
#              /         \                           /         \
#           < /           \ >=                    < /           \ >=
#            /             \                       /             \
#  node_for(target)    next_step               next_step    node_for(target)
#
# Each node tracks the ranges of x, m, a and s values that a part can have if it reached
# this node - the root node can see all parts, and each branch node splits the relevant
# variable's range at the threshold sending the left part to the < child and the right part
# to the >= child.  This also means we can prune nodes as we build the tree - if the
# threshold for this test falls outside the current range of the target variable then the
# test will always succeed or always fail, so we can replace the branch entirely with its
# left or right child as appropriate.
#
# This also means that part 2 can be calculated trivially from the product of the range
# sizes for every Leaf node in the final tree.

@dataclass
class Node:
    x: range
    m: range
    a: range
    s: range

    parent: "Node"


@dataclass
class Branch(Node):
    var: str = None
    threshold: int = None
    lt_node: Node = None
    ge_node: Node = None

    def test(self, part):
        if part[self.var] < self.threshold:
            return self.lt_node.test(part)
        else:
            return self.ge_node.test(part)


@dataclass
class Leaf(Node):
    accept: bool

    def test(self, part):
        return self.accept


Step = namedtuple("Step", ["var", "op", "val", "target"])


@dataclass
class Workflow:
    """Intermediate representation of the workflow sequences before compiling them into
    the final tree"""
    name: str
    steps: list[Step]


def parse_input():
    parts = []

    with open("input", "r") as f:
        workflows = {}
        itr = iter(f)
        line = next(itr).strip()
        while line:
            name, _, rest = line.partition("{")
            steps_text = rest[:-1].split(",")
            steps = []
            for s in steps_text:
                if ":" in s:
                    expr, tgt = s.split(":", 1)
                    steps.append(Step(expr[0], expr[1], int(expr[2:]), tgt))
                else:
                    steps.append(Step(None, None, None, s))
            workflows[name] = Workflow(name, steps)
            line = next(itr).strip()

        # remaining lines are parts
        for line in itr:
            line = line.strip()
            part = {}
            for item in line[1:-1].split(","):
                k, v = item.split("=", maxsplit=1)
                part[k] = int(v)
            parts.append(part)

    print(f"Before simplification, {len(workflows)} workflows")
    # Simplify as follows, repeatedly until nothing changes:
    state = "\n".join([repr(w) for w in workflows])
    last_state = None
    while state != last_state:
        simplified_workflows = 0
        for w in workflows.values():
            # if the target of the last conditional step in a workflow is the same as the final
            # default target (e.g. {x<500:R,m>3000:A,A}) then the conditional step is redundant
            # (this workflow is equivalent to {x<500:R,A}).
            changed_w = False
            while len(w.steps) > 1 and w.steps[-2].target == w.steps[-1].target:
                changed_w = True
                w.steps.pop(-2)
            if changed_w:
                simplified_workflows += 1
        print(f"Simplified {simplified_workflows} workflows")

        # if any workflow reduces down to a single step (e.g. xyz{R}, abc{A} or def{ghi}) then
        # replace its call site(s) with that single step
        trivial_workflows = {k: w.steps[0].target for k, w in workflows.items() if len(w.steps) == 1}
        print(f"Removed {len(trivial_workflows)} trivial workflows")
        for k in trivial_workflows:
            del workflows[k]
        for w in workflows.values():
            for i in range(len(w.steps)):
                if w.steps[i].target in trivial_workflows:
                    w.steps[i] = Step(w.steps[i].var, w.steps[i].op, w.steps[i].val,
                                      trivial_workflows[w.steps[i].target])

        # if the last step of a workflow is an unconditional branch to another workflow, concatenate
        # the second workflow's steps to the first - once this is fully resolved every workflow should
        # end with either ",A" or ",R"
        joined_workflows = 0
        for w in workflows.values():
            last_step_target = w.steps[-1].target
            if last_step_target not in ("A", "R"):
                joined_workflows += 1
                w.steps[-1:] = workflows[last_step_target].steps
        print(f"Joined {joined_workflows} step lists")

        last_state = state
        state = "\n".join([repr(w) for w in workflows.values()])

    print(f"After simplification, {len(workflows)} workflows")

    print("Building graph")

    def node_for_target(target, parent, ranges):
        if target == "A":
            return Leaf(**ranges, parent=parent, accept=True)
        if target == "R":
            return Leaf(**ranges, parent=parent, accept=False)

        return to_node(workflows[target].steps, parent, ranges)

    def to_node(steps, parent, ranges):
        step = steps[0]
        if step.var is None:
            # given the earlier simplification, this will always be a leaf node A or R
            return node_for_target(step.target, parent, ranges)

        if step.val not in ranges[step.var]:
            # This step's test will either always succeed or always fail, as the threshold
            # is outside the range of possible values for the target variable on parts that
            # could have reached this node.  Work out which it is
            if (
                    (step.op == "<" and step.val < ranges[step.var].start) or
                    (step.op == ">" and step.val >= ranges[step.var].stop)
            ):
                # test always fails - go to the next step
                return to_node(steps[1:], parent, ranges)
            else:
                # test always succeeds - go to target
                return node_for_target(step.target, parent, ranges)

        # We've established that we do need to branch here
        node = Branch(**ranges, parent=parent, var=step.var, threshold=step.val)
        if step.op == "<":
            # left branch if succeeds
            new_ranges = dict(ranges)
            new_ranges[step.var] = range(new_ranges[step.var].start, node.threshold)
            node.lt_node = node_for_target(step.target, node, new_ranges)

            # right branch if fail
            new_ranges = dict(ranges)
            new_ranges[step.var] = range(node.threshold, new_ranges[step.var].stop)
            node.ge_node = to_node(steps[1:], node, new_ranges)
        else:  # >
            node.threshold = step.val + 1

            # left branch if fail
            new_ranges = dict(ranges)
            new_ranges[step.var] = range(new_ranges[step.var].start, node.threshold)
            node.lt_node = to_node(steps[1:], node, new_ranges)

            # right branch if succeeds
            new_ranges = dict(ranges)
            new_ranges[step.var] = range(node.threshold, new_ranges[step.var].stop)
            node.ge_node = node_for_target(step.target, node, new_ranges)

        return node

    # Start with the "in" workflow, which has no parent and is reachable by all xmas values
    root = to_node(workflows["in"].steps, None, dict(x=range(1, 4001), m=range(1, 4001),
                   a=range(1, 4001), s=range(1, 4001)))

    return root, parts


def total_value():
    root, parts = parse_input()
    total = 0
    for part in parts:
        if root.test(part):
            total += sum(part.values())

    return total


def possible_combinations():
    root, _ = parse_input()
    combinations = 0

    def acceptors(node):
        if isinstance(node, Leaf):
            if node.accept:
                yield node
        else:
            yield from acceptors(node.lt_node)
            yield from acceptors(node.ge_node)

    for node in acceptors(root):
        combinations += len(node.x) * len(node.m) * len(node.a) * len(node.s)

    return combinations


if __name__ == "__main__":
    print(f"Total value of parts: {total_value()}")
    print(f"Total possible combinations: {possible_combinations()}")
