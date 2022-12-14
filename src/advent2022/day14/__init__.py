import sys
import copy
from collections import deque

def pairs(it):
    if not hasattr(it, "__next__"):
        it = iter(it)
    try:
        swap = next(it)
        for item in it:
            yield swap, item
            swap = next(it)
            yield item, swap
    except StopIteration:
        pass

def in_range(coord, range):
    return range[0] <= coord < range[1]

def in_bounds(cave, point, col_range):
    return point[0] < len(cave) and in_range(point[1], col_range)

def lookup(cave, point, col_range):
    return cave[point[0]][point[1] - col_range[0]]

def simulate_sand(cave, sand, col_range):
    while in_bounds(cave, sand, col_range):
        for fall_point in (
                (sand[0] + 1, sand[1]), # down
                (sand[0] + 1, sand[1] - 1), # down-left
                (sand[0] + 1, sand[1] + 1), # down-right
            ):
            if not in_bounds(cave, fall_point, col_range):
                return None # sand falls into the void
            if lookup(cave, fall_point, col_range) == '.':
                sand = fall_point
                break
        else:
            return sand
    return None

def simulate_sand2(cave, sand, col_range):
    while True:
        if sand[0] + 1 >= len(cave): # hit the flo'
            return sand
        for fall_point in (
                (sand[0] + 1, sand[1]), # down
                (sand[0] + 1, sand[1] - 1), # down-left
                (sand[0] + 1, sand[1] + 1), # down-right
            ):
            # expand our mind as necessary
            if fall_point[1] < col_range[0]:
                col_range[0] -= 1
                for row in cave:
                    row.appendleft('.')
            elif fall_point[1] >= col_range[1]:
                col_range[1] += 1
                for row in cave:
                    row.append('.')
            if lookup(cave, fall_point, col_range) == '.':
                sand = fall_point
                break # continue falling
        else:
            return sand # could not fall
    return None

def dump_cave(cave, col_range):
    print()
    for digit in range(2, -1, -1):
        print("   ", end="")
        for col in range(*col_range):
            print(" ", end="")
            print((col % 10**(digit+1)) // 10**digit, end="")
        print()
    for row in range(len(cave)):
        print(f"{row:3d}", " ".join(cave[row]))
    print()

def main(stream, opts):
    rocklines = []
    row_range = [sys.maxsize, 0]
    col_range = [sys.maxsize, 0]

    for line in stream:
        parts = line.split(" -> ")
        rocklines.append([tuple(int(x) for x in part.split(",")) for part in parts])
        for col, row in rocklines[-1]:
            if col < col_range[0]:
                col_range[0] = col
            if col > col_range[1]:
                col_range[1] = col
            if row < row_range[0]:
                row_range[0] = row
            if row > row_range[1]:
                row_range[1] = row

    row_range[1] += 1
    col_range[1] += 1
    #col_span = col_range[1] - col_range[0]
    #row_span = row_range[1] - row_range[0]
    cave = [["." for col in range(*col_range)] for row in range(0, row_range[1]) ]

    for rockline in rocklines:
        for start, end in pairs(rockline):
            if start[0] == end[0]:
                span_index = 1
            elif start[1] == end[1]:
                span_index = 0
            else:
                raise AssertionError("not expecting diagonal rock lines")
            const_index = span_index ^ 1
            const = start[const_index]
            sgn = 1 if end[span_index] > start[span_index] else -1
            coordrange = range(start[span_index], end[span_index] + sgn, sgn)
            for coord in coordrange:
                if span_index == 1:
                    row = coord
                    col = const
                else:
                    row = const
                    col = coord
                cave[row][col - col_range[0]] = '#'

    if opts.verbose:
        dump_cave(cave, col_range)

    cave2 = [deque(row) for row in cave]
    sand_in = (0, 500)

    try:
        # part 1:
        sand_out = sand_in
        step = 0
        while sand_out is not None:
            sand_out = simulate_sand(cave, sand_in, col_range)
            if opts.verbose:
                print(f"step {step:3d}: sand fell to {sand_out}")
            if sand_out is not None:
                cave[sand_out[0]][sand_out[1] - col_range[0]] = 'o'
                step += 1

        if opts.verbose:
            dump_cave(cave2, col_range)

        print("part 1:", step)

        # part 2 -- add space above floor, floor will be inferred in simulation
        cave2.append(deque("." for col in range(*col_range)))
        sand_out = None
        step = 0
        while sand_out != sand_in:
            sand_out = simulate_sand2(cave2, sand_in, col_range)
            if opts.verbose:
                print(f"step {step:3d}: sand fell to {sand_out}")
            if sand_out is not None:
                cave2[sand_out[0]][sand_out[1] - col_range[0]] = 'o'
            step += 1

        if opts.verbose:
            dump_cave(cave2, col_range)

        print("part 2:", step)

    except KeyboardInterrupt:
        if opts.verbose:
            dump_cave(cave2, col_range)
