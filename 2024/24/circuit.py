from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Gate:
    name: str
    a: bool | None
    b: bool | None
    op: str
    outputs: list[tuple["Gate", str]]

    def ready(self):
        return self.a is not None and self.b is not None

    def reset(self):
        self.a = None
        self.b = None

    def run(self):
        if self.a is None or self.b is None:
            raise ValueError(f"Incomplete inputs for node {self.name}")

        match self.op:
            case "OR":
                value = self.a or self.b
            case "AND":
                value = self.a and self.b
            case "XOR":
                value = self.a != self.b
            case _:
                value = self.a

        ready_children = []
        for node, attr in self.outputs:
            setattr(node, attr, value)
            if node.ready():
                ready_children.append(node)

        return ready_children


class Output(Gate):
    output: int = 0
    mask: int = 0
    target_mask: int = 0

    def __setattr__(self, key, value):
        if key.startswith("z"):
            idx = int(key[1:])
            self.output |= int(value) << idx
            self.mask |= 1 << idx
        else:
            super().__setattr__(key, value)

    def ready(self):
        return self.mask == self.target_mask

    def run(self):
        print(f"final value: {self.output}")
        return []


def load_data():
    with open("input", "r") as f:
        inputs = {}
        for line in f:
            line = line.strip()
            if not line:
                break
            fields = line.split(": ")
            inputs[fields[0]] = bool(int(fields[1]))

        in_gates = {name: Gate(name, val, val, "AND", []) for name, val in inputs.items()}
        gates = in_gates.copy()
        out_gates = {}
        links = defaultdict(list)
        for line in f:
            (a, op, b, _, name) = line.strip().split(maxsplit=4)
            g = Gate(name, None, None, op, [])
            gates[name] = g
            if name.startswith("z"):
                out_gates[name] = g
            if name in inputs:
                in_gates[name] = g
            links[a].append((g, "a"))
            links[b].append((g, "b"))

        # connect the dots
        for name, outputs in links.items():
            gates[name].outputs = outputs

        output = Output("z", None, None, "OUT", [])
        target_mask = 0
        for name, gate in out_gates.items():
            gate.outputs.append((output, name))
            target_mask |= 1 << int(name[1:])

        output.target_mask = target_mask

    return in_gates, gates, output


def part1():
    in_gates, gates, output = load_data()

    ready_gates = list(in_gates.values())
    while ready_gates:
        g = ready_gates.pop(0)
        ready_children = g.run()
        ready_gates.extend(ready_children)


if __name__ == "__main__":
    part1()