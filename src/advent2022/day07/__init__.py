
class file:
    def __init__(self, name, size):
        self.name = name
        self.size = size
    def __repr__(self):
        print(self.size, self.name)

class dir:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.dirs = dict()
        self.files = list()
        self._size = None
    def size(self):
        if self._size is None: # memoize
            self._size = sum(file.size for file in self.files) + sum(
                self.dirs[dir].size() for dir in self.dirs
            )
        return self._size
    def make_dir(self, subdir):
        if subdir not in self.dirs:
            self.dirs[subdir] = dir(subdir, self)
        return self.dirs[subdir]
    def add_file(self, filename, size):
        self.files.append(file(filename, size))
    def path(self):
        parts = list()
        current = self
        while current is not None:
            parts.append(current.name)
            current = current.parent
        return "/".join(reversed(parts))
    def root(self):
        current = self
        while current.parent is not None:
            current = current.parent
        return current
    def dfs(self, v):
        for dir in self.dirs.values():
            result = dir.dfs(v)
            if result is not None:
                return result
        return self if v(self) else None

def main(stream, opts):
    cwd = root = dir("")
    line = stream.readline()
    while line:
        if line[0] != "$": # command
            raise RuntimeError(f"expected command, not {line[:-1]!r}")
        cmd = line[2:4]
        if opts.verbose:
            print("$", cmd)
        if cmd == "cd": # change dir
            path = line[5:-1] # strip newline
            if path == "..":
                cwd = cwd.parent
            elif path == "/":
                cwd = root
            else:
                cwd = cwd.make_dir(path)
            line = stream.readline()
        elif cmd == "ls": # list
            line = stream.readline()
            while line:
                if line.startswith("dir "):
                    cwd.make_dir(path)
                elif line[0] == "$":
                    break
                else:
                    size, name = line.split(None, 1)
                    cwd.add_file(name.rstrip(), int(size))
                line = stream.readline()
        else:
            raise RuntimeError(f"unsupported command {cmd!r}")

    p1sum = [0]
    def visit(d):
        if d.size() <= 100000:
            p1sum[0] += d.size()
    root.dfs(visit)
    print("part 1:", p1sum[0])

    total_space = 70000000
    free_target = 30000000
    free_current = (total_space - root.size())
    need_freed = free_target - free_current
    print(f"need to free {need_freed}")
    best_removal = [root]
    def visit(d):
        if d.size() >= need_freed and d.size() < best_removal[0].size():
            if opts.verbose:
                print(f"{d.name}, size={d.size()} >= need_freed {need_freed}?")
            best_removal[0] = d
    root.dfs(visit)
    best_removal = best_removal[0]
    print("part 2:", best_removal.name, best_removal.size())
