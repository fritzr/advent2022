from itertools import chain
from collections import deque

def main(stream, opts):
    # build crate stacks.
    first_line = stream.readline()[:-1] # strip newline
    p1stacks = [deque() for _ in range((len(first_line) + 1) // 4)]
    for line in chain((first_line,), stream):
        line = line[:-1]
        if not line or "[" not in line:
            stream.readline() # skip crate indexes
            break
        for crate_id, crate_index in enumerate(range(0, len(line), 4)):
            crate = line[crate_index:crate_index+3].strip()
            if crate:
                p1stacks[crate_id].appendleft(crate[1:-1]) # strip '[]'

    if opts.verbose:
        for index, stack in enumerate(p1stacks):
            print(f"{index+1:2d}  [" + "] [".join(stack) + "]")

    p2stacks = [deque(stack) for stack in p1stacks]

    # simulate crate instructions: "move X from Y to Z"
    for line in stream:
        words = line.split()
        quantity = int(words[1])
        source = int(words[3]) - 1
        dest = int(words[5]) - 1
        # move crates one at a time for p1
        for _ in range(quantity):
            p1stacks[dest].append(p1stacks[source].pop())
        # move all crates at a time (reverse the pop order) for p2
        p2stacks[dest].extend(
            reversed(tuple(p2stacks[source].pop() for _ in range(quantity)))
        )

    print("part1:", "".join(stack[-1] for stack in p1stacks))
    print("part2:", "".join(stack[-1] for stack in p2stacks))
