import sys

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
    cave = [["." for col in range(*col_range)] for row in range(*row_range) ]

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
                cave[row - row_range[0]][col - col_range[0]] = '#'

    if opts.verbose:
        for row in range(*row_range):
            print(f"{row:3d}", " ".join(cave[row - row_range[0]]))
