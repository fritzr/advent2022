import numpy as np

#
#    0,0   0,1   0,2   0,3
#    1,0
#    2,0   ...   ...   n,n
#

directions = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}

ROW, COL = 0, 1

def move_tail(head, tail):
    diff = head - tail
    if all(abs(diff) <= 1): # adjacent: keep position
        return
    # move one unit cardinally and possibly diagonally towards head
    if head[ROW] == tail[ROW]:
        tail[COL] += 1 if diff[COL] > 0 else -1
    elif head[COL] == tail[COL]:
        tail[ROW] += 1 if diff[ROW] > 0 else -1
    # move one unit diagonally towards head
    else:
        tail[ROW] += 1 if diff[ROW] > 0 else -1
        tail[COL] += 1 if diff[COL] > 0 else -1

def simulate_rope(instructions, nknots, opts):
    knots = [np.array((0, 0)) for _ in range(nknots)]
    visited = set(((0, 0),))

    for instruction in instructions:
        direction = directions[instruction[0]]
        magnitude = int(instruction[2:])
        if opts.verbose:
            print("MOVE", instruction[:-1])
        for _ in range(magnitude):
            knots[0] += direction
            for index, tails in enumerate(knots[1:]):
                move_tail(knots[index], knots[index+1])
            if opts.verbose:
                print("knots: ", "  ".join(map(str, knots)))
            visited.add(tuple(knots[-1]))
    return visited

def main(stream, opts):
    head = np.array((0, 0))
    tail = np.array((0, 0))
    visited = set((tuple(tail),))

    instructions = stream.readlines()
    print("part 1: tail visited", len(simulate_rope(instructions, 2, opts)))
    print("part 2: tail visited", len(simulate_rope(instructions, 10, opts)))
