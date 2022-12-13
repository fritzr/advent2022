IN_ORDER = -1
OK = 0
OUT_OF_ORDER = 1

def compare(a, b):
    if isinstance(a, int) and isinstance(b, int):
        if a < b:
            return IN_ORDER
        if a > b:
            return OUT_OF_ORDER
        return OK
    if isinstance(a, list) and isinstance(b, list):
        for aitem, bitem in zip(a, b):
            result = compare(aitem, bitem)
            if result != OK:
                return result
        return compare(len(a), len(b))
    if isinstance(a, int):
        return compare([a], b)
    if isinstance(b, int):
        return compare(a, [b])
    assert(False)

class Packet(list):
    def __new__(self, _):
        return list.__new__(self)
    def __init__(self, text):
        list.__init__(self, eval(text))

    def __lt__(self, o):
        return compare(self, o) == IN_ORDER
    def __gt__(self, o):
        return compare(self, o) == OUT_OF_ORDER
    def __eq__(self, o):
        return list(self) == list(o)

    def __repr__(self):
        return f"{type(self).__name__}({list(self)!r})"

def main(stream, opts):
    inorder_val = 0
    all_packets = []
    for index, pairstr in enumerate(stream.read().split("\n\n")):
        lines = pairstr.split("\n")[:2]
        alist = Packet(lines[0])
        blist = Packet(lines[1])
        all_packets.extend((alist, blist))
        if alist < blist:
            inorder_val += index + 1

    print("part 1:", inorder_val)

    all_packets.extend(([[2]], [[6]]))
    sorted_packets = sorted(all_packets)
    print("part 2:",
        (1 + sorted_packets.index([[2]]))
        * (1 + sorted_packets.index([[6]]))
    )
