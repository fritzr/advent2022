from collections import deque
from operator import mul, add
from functools import reduce

operands = {
    "*": mul,
    "+": add,
}

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

    def finish_op(self, num):
        return num // 3

    def inspect(self):
        while self.items:
            self.inspections += 1
            item = self.items.popleft()
            item = self.finish_op(self.do_op(item))
            yield item, (self.true_monkey if item % self.test == 0 else self.false_monkey)

class ModMonkey(Monkey):
    @classmethod
    def clone(cls, o, divisor):
        return cls(
            divisor, o.id, o.items, (o.lop, o.op, o.rop), o.test,
            o.true_monkey, o.false_monkey
        )

    def __init__(self, divisor, *args):
        super().__init__(*args)
        self.divisor = divisor

    def finish_op(self, num):
        return num % self.divisor

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
    divisor = reduce(mul, (monkey.test for monkey in monkeys))
    mod_monkeys = [ModMonkey.clone(monkey, divisor) for monkey in monkeys]

    for _ in range(20):
        monkey_around(monkeys)
    print("part 1:", monkey_business(monkeys))

    for _ in range(10000):
        monkey_around(mod_monkeys)
    print("part 2:", monkey_business(mod_monkeys))
