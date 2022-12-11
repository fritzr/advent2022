from collections import deque
from operator import mul, add

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

    def inspect(self):
        while self.items:
            item = self.items.popleft()
            item = self.op(
                item if self.lop == "old" else self.lop,
                item if self.rop == "old" else self.rop,
            ) // 3
            yield item, (self.true_monkey if item % self.test == 0 else self.false_monkey)

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

    num_inspections = [0] * len(monkeys)
    for _ in range(20):
        for monkey in monkeys:
            for worry, next_monkey in monkey.inspect():
                num_inspections[monkey.id] += 1
                monkeys[next_monkey].items.append(worry)

    print("part 1:", mul(*sorted(num_inspections)[-2:]))
