from functools import partial


monkeys = []
modulus = 1
debug = False


def dbg(*args):
    if debug:
        print(*args)


class Monkey:
    def __init__(self, items, op, divisor, target_true, target_false):
        self.items = items
        self.op = op
        self.divisor = divisor
        self.target_true = target_true
        self.target_false = target_false
        self.inspections = 0

    def take_turn(self, divide_worry=1):
        dbg(f"I have {self.items}")
        while self.items:
            item = self.items.pop(0)
            self.inspections += 1
            worry = item
            dbg(f"Initial worry: {worry}")
            # Monkey inspects item
            worry = self.op(worry)
            dbg(f"After inspection {worry}")
            # Phew, they didn't damage it
            worry = worry // divide_worry
            dbg(f"After relief {worry}")
            # Keep the worry levels from escalating too far - the input has been designed
            # so that the "divisible by" numbers for each monkey are all co-prime (in fact
            # all prime) so we can safely work modulo their product without changing the
            # result.
            worry = worry % modulus
            dbg(f"After modulo {worry}")
            # Where to throw it next
            divisible = (worry % self.divisor == 0)
            if divisible:
                dbg(f"Divisible by {self.divisor} - throwing to {self.target_true}")
                monkeys[self.target_true].catch(worry)
            else:
                dbg(f"Not divisible by {self.divisor} - throwing to {self.target_false}")
                monkeys[self.target_false].catch(worry)
        dbg(f"Turn complete, total inspections now {self.inspections}")

    def catch(self, item):
        self.items.append(item)


def add(x, y):
    return x + y


def mult(x, y):
    return x * y


def parse_input():
    global modulus
    with open("input", "r") as f:
        itr = iter(f)
        for line in itr:
            if not line:
                continue
            if line.startswith("Monkey"):
                items = [int(i) for i in next(itr).strip()[len("Starting items: "):].split(", ")]

                op_line = next(itr).strip()[len("Operation: new = old "):]
                operator, operand = op_line.split(maxsplit=1)
                if operand == "old":
                    if operator == "*":
                        op = lambda w: w * w
                    else:  # +
                        op = lambda w: w + w
                else:
                    delta = int(operand)
                    if operator == "*":
                        op = partial(mult, delta)
                    else:  # +
                        op = partial(add, delta)

                divisor = int(next(itr).strip()[len("Test: divisible by "):])
                target_true = int(next(itr).strip()[len("If true: throw to monkey "):])
                target_false = int(next(itr).strip()[len("If false: throw to monkey "):])
                monkeys.append(Monkey(items, op, divisor, target_true, target_false))

                # Keep the worry levels from escalating too far - the input has been designed
                # so that the "divisible by" numbers for each monkey are all co-prime (in fact
                # all prime) so we can safely work modulo their product without changing the
                # result.
                modulus *= divisor


def run(iterations, divide_worry):
    parse_input()
    dbg(monkeys)

    for i in range(iterations):
        for j, monkey in enumerate(monkeys):
            dbg(f"Round {i} monkey {j}")
            monkey.take_turn(divide_worry)

    # order monkeys by number of inspections
    sorted_monkeys = sorted(monkeys, key=lambda m: m.inspections, reverse=True)
    print(f"Top two monkeys inspected {sorted_monkeys[0].inspections} and {sorted_monkeys[1].inspections} items")
    print(f"Monkey business = {sorted_monkeys[0].inspections * sorted_monkeys[1].inspections}")


if __name__ == "__main__":
    run(20, 3)

    monkeys = []
    modulus = 1
    run(10000, 1)
