
def priority(char):
    code = ord(char)
    if code >= ord('a') and code <= ord('z'):
        return code - ord('a') + 1
    return code - ord('A') + 27

def correct_sack(sack, opts):
    compartments = len(sack) // 2
    sack1 = set()
    sack2 = set()
    for pos1, pos2 in zip(range(compartments), range(compartments, len(sack))):
        char1, char2 = sack[pos1], sack[pos2]
        sack1.add(char1)
        sack2.add(char2)
        for char in (char1, char2):
            if char in sack1 and char in sack2:
                pri = priority(char)
                if opts.verbose:
                    print(f"{char} -> priority {pri}")
                return pri

def find_common(groups):
    common = set(groups[0])
    for group in groups[1:]:
        common = common.intersection(group)
    return common

def main(stream, opts):
    lines = [line.strip() for line in stream.readlines()]

    prisum = 0
    for line in lines:
        prisum += correct_sack(line, opts)
    print("part 1:", prisum)

    prisum = 0
    for line_start in range(0, len(lines), 3):
        common = find_common(lines[line_start:line_start+3])
        assert(len(common) == 1)
        prisum += priority(common.pop())
    print("part 2:", prisum)
