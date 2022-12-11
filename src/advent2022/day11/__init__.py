from collections import deque
from operator import mul, add

operands = {
    "*": mul,
    "+": add,
}

class ModSet:
    def __init__(self, num, divisors):
        self.mods = dict((divisor, (num % divisor)) for divisor in divisors)

    def transform(self, func):
        for divisor, remainder in self.mods.items():
            self.mods[divisor] = func(remainder) % divisor

    def divisible(self, divisor):
        return self.mods[divisor] == 0

    def __repr__(self):
        return f"{type(self).__name__}({self.mods!r})"

class Monkey:
    def __init__(self, id, items, op, test, true_monkey, false_monkey):
        self.id = id
        self.items = deque(items)
        self.lop, self.op, self.rop = op
        self.test = test
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey
        self.inspections = 0

    def do_op(self, num):
        return self.op(
            num if self.lop == "old" else self.lop,
            num if self.rop == "old" else self.rop,
        )

    def inspect(self):
        while self.items:
            self.inspections += 1
            item = self.items.popleft()
            item = self.do_op(item) // 3
            yield item, (self.true_monkey if item % self.test == 0 else self.false_monkey)

class ModMonkey(Monkey):
    @classmethod
    def clone(cls, o, divisors):
        return cls(
            divisors, o.id, o.items, (o.lop, o.op, o.rop), o.test,
            o.true_monkey, o.false_monkey
        )

    def __init__(self, divisors, *args):
        super().__init__(*args)
        self.items = deque(ModSet(item, divisors) for item in self.items)

    def inspect(self):
        while self.items:
            self.inspections += 1
            modset = self.items.popleft()
            modset.transform(self.do_op)
            yield modset, (
                self.true_monkey if modset.divisible(self.test) else self.false_monkey
            )

def monkey_around(monkeys):
    for monkey in monkeys:
        for worry, next_monkey in monkey.inspect():
            monkeys[next_monkey].items.append(worry)

def monkey_business(monkeys):
    inspections = [monkey.inspections for monkey in monkeys]
    return mul(*sorted(inspections)[-2:])

def main(stream, opts):
    monkeys = []
    for monkey_id, monkey in enumerate(stream.read().split("\n\n")):
        lines = iter(monkey.split("\n"))
        # monkey_id
        next(lines)
        items = [int(item.strip()) for item in next(lines).split(":", 1)[1].split(",")]
        lhs, op, rhs = next(lines).split("=", 1)[1].split(None, 3)
        if lhs != "old":
            lhs = int(lhs)
        if rhs != "old":
            rhs = int(rhs)
        op = operands[op.strip()]
        test = int(next(lines).split("by", 1)[1].strip())
        true_monkey = int(next(lines).split("monkey", 1)[1].strip())
        false_monkey = int(next(lines).split("monkey", 1)[1].strip())
        monkeys.append(Monkey(
            monkey_id, items, (lhs, op, rhs), test, true_monkey, false_monkey
        ))

    # initialize smarter phase 2 monkes
    divisors = [monkey.test for monkey in monkeys]
    mod_monkeys = [ModMonkey.clone(monkey, divisors) for monkey in monkeys]

    for _ in range(20):
        monkey_around(monkeys)
    print("part 1:", monkey_business(monkeys))

    for _ in range(10000):
        monkey_around(mod_monkeys)
    print("part 2:", monkey_business(mod_monkeys))
