from collections import namedtuple
Signal = namedtuple("Signal", ["level", "dest"])


class Module:
    name: str
    children: list[str]

    def __init__(self, name, children):
        self.name = name
        self.children = children

    def __repr__(self):
        return f"{type(self)}: {self.name} -> {self.children}"

    def handle_pulse(self, level, src):
        """
        Handle a pulse.
        :param level: level of the pulse - True = high, False = low
        :param src: module from which the pulse was sent
        :return: iterable of (level, dest) pairs for the pulses that should be sent as
        a result of handling this pulse
        """
        return
        yield None  # Unreachable, only exists to make the compiler treat this method as a generator

    def send(self, level):
        """
        Send a pulse of the specified level to each child
        :param level: the level
        :return: generator yielding (level, child) for each child - handle_pulse will
        typically "yield from self.send(level)"
        """
        for c in self.children:
            yield Signal(level, c)

    def connect_from(self, src):
        """
        Add an incoming connection to this module from another module.
        :param src: the name of the module from which the connection originates
        """
        pass

    def reset(self):
        """
        Reset this module to its initial state.
        """
        pass


class FlipFlopModule(Module):
    state: bool

    def __init__(self, name, children):
        super().__init__(name, children)
        self.state = False

    def handle_pulse(self, level, src):
        if level:
            # flipflop ignores high pulses
            return

        # low pulses flip state
        self.state = not self.state
        # and send pulses for the new state
        yield from self.send(self.state)

    def reset(self):
        self.state = False


class ConjunctionModule(Module):
    parents: list[str]
    last_seen: dict[str, bool]

    def __init__(self, name, children):
        super().__init__(name, children)
        self.parents = []
        self.last_seen = {}

    def connect_from(self, src):
        self.parents.append(src)
        self.last_seen[src] = False

    def reset(self):
        for k in self.last_seen:
            self.last_seen[k] = False

    def handle_pulse(self, level, src):
        self.last_seen[src] = level

        if all(self.last_seen.values()):
            # all high -> send low
            yield from self.send(False)
        else:
            # not all high -> send high
            yield from self.send(True)

    def __repr__(self):
        return f"{super().__repr__()} (from {self.parents})"


class BroadcastModule(Module):
    def handle_pulse(self, level, src):
        yield from self.send(level)


MODULES: dict[str, Module] = {}


def parse_input():
    used_outputs = set()
    with open("input", "r") as f:
        for line in f:
            line = line.strip()
            mod, _, outputs = line.partition(" -> ")
            outputs = outputs.split(", ")
            used_outputs.update(outputs)
            if mod == "broadcaster":
                MODULES[mod] = BroadcastModule(mod, outputs)
            elif mod.startswith("%"):
                mod = mod[1:]
                MODULES[mod] = FlipFlopModule(mod, outputs)
            elif mod.startswith("&"):
                mod = mod[1:]
                MODULES[mod] = ConjunctionModule(mod, outputs)

    # add undeclared output modules
    for module in used_outputs:
        if module not in MODULES:
            MODULES[module] = Module(module, [])

    # link the modules together
    for name, module in MODULES.items():
        for child in module.children:
            MODULES[child].connect_from(name)

    # print(MODULES)


def press_button():
    num_low = 1
    num_high = 0
    # button sends a low to the broadcaster
    signals = [("button", Signal(False, "broadcaster"))]
    while len(signals) > 0:
        this_src, this_signal = signals.pop(0)
        # print(f"Handling {this_src} -> {this_signal}")
        for new_signal in MODULES[this_signal.dest].handle_pulse(this_signal.level, this_src):
            if new_signal.level:
                num_high += 1
            else:
                num_low += 1
            signals.append((this_signal.dest, new_signal))

    return num_high, num_low


def push_many_times(n):
    total_high = 0
    total_low = 0
    for i in range(n):
        high, low = press_button()
        # debugging for part 2 - dump representation of flipflop states in binary
        # print(f"{i+1:4d} {''.join('1' if x.state else '0' for x in MODULES.values() if isinstance(x, FlipFlopModule))}")
        total_high += high
        total_low += low

    print(total_high, total_low)
    return total_high * total_low


if __name__ == "__main__":
    parse_input()
    print(f"Pulses sent after 1000 pushes: {push_many_times(1000)}")
