import sys
from heapq import *

class Grid:
    def __init__(self, dim, value=0, data=None):
        self.nrows, self.ncols = dim
        if data is not None:
            self.data = data
        else:
            self.data = [[value] * self.ncols for _ in range(self.nrows)]

    def adjacent(self, pos):
        for rowd, cold in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            new = (pos[0] + rowd, pos[1] + cold)
            if (0 <= new[0] < self.nrows and 0 <= new[1] < self.ncols):
                yield new

    def __getitem__(self, pos):
        return self.data[pos[0]][pos[1]]

    def __setitem__(self, pos, value):
        self.data[pos[0]][pos[1]] = value

    def __iter__(self):
        for row in self.data:
            yield row

class PathGrid(Grid):
    @classmethod
    def parse(cls, lines):
        data = []
        start = (-1, -1)
        end = (-1, -1)
        for row, line in enumerate(lines):
            if line:
                data.append(line)
                for col, c in enumerate(line):
                    if c == ord("S"):
                        start = (row, col)
                    elif c == ord("E"):
                        end = (row, col)
        return cls((len(data), len(data[0])), data, start, end)

    def __init__(self, dim, data, start, end, climb=True):
        super().__init__(dim, data=data)
        self.data = data
        self.start = start
        self.end = end
        self.climb = climb

    height_trans = {
        ord("S"): ord("a"),
        ord("E"): ord("z"),
    }

    def adjacent(self, pos):
        for adj in super().adjacent(pos):
            cur_height = self.height_trans.get(self[pos], self[pos])
            next_height = self.height_trans.get(self[adj], self[adj])
            if (self.climb and next_height <= cur_height + 1) or (
                    not self.climb and next_height >= cur_height - 1):
                yield adj

    class _heapnode:
        def __init__(self, grid, pos, distance=sys.maxsize):
            self.grid = grid
            self.pos = pos
            self.distance = distance
        def __lt__(self, onode):
            return self.distance < onode.distance
        def char(self):
            return chr(self.grid[self.pos])
        def __repr__(self):
            return f"heapnode({self.pos!r}*{self.distance} '{self.char()}')"

    def shortest_distance(self, start, endfunc, up, opts):
        distance = Grid((self.nrows, self.ncols))
        paths = Grid((self.nrows, self.ncols), value=None)
        visited_set = set()
        unvisited = []
        for row in range(self.nrows):
            for col in range(self.ncols):
                node = self._heapnode(
                    self, (row, col), 0 if start == (row, col) else sys.maxsize
                )
                heappush(unvisited, node)
                distance[(row, col)] = node
        while unvisited:
            # XXX: use decrease_priority() instead of re-heapifying every time
            heapify(unvisited)
            current = heappop(unvisited)
            #if opts.verbose:
            #    print(f"visiting {current}")
            if endfunc(current.pos):
                break
            for neighbor in self.adjacent(current.pos):
                if neighbor not in visited_set:
                    new_dist = distance[current.pos].distance + 1
                    if distance[neighbor].distance > new_dist:
                        #if opts.verbose:
                        #    print(f"neighbor {neighbor}: new distance"
                        #        f" {distance[neighbor].distance} -> {new_dist}")
                        distance[neighbor].distance = new_dist
                        paths[neighbor] = current.pos
            visited_set.add(current.pos)

        if opts.verbose:
            path = [current.pos]
            parent = current.pos
            while parent != start:
                path.append(parent)
                parent = paths[parent]
            print("path:", list(reversed(path)))

        return distance[current.pos].distance

def main(stream, opts):
    grid = PathGrid.parse(stream.read().encode().split(b"\n"))

    if opts.verbose:
        for row in grid:
            print(row.decode())
        print(f"start at {grid.start}, end at {grid.end}")

    grid.climb = True
    print("part 1:",
        grid.shortest_distance(grid.start, lambda pos: pos == grid.end, True, opts)
    )

    grid.climb = False
    print("part 2:",
        grid.shortest_distance(grid.end, lambda pos: grid[pos] == ord("a"), False, opts)
    )
