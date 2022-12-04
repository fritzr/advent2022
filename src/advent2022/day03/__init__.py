
def priority(char):
    code = ord(char)
    if code >= ord('a') and code <= ord('z'):
        return code - ord('a') + 1
    return code - ord('A') + 27

def correct_sack(line, opts):
    compartments = len(line) // 2
    sack1 = set()
    sack2 = set()
    for pos1, pos2 in zip(range(compartments), range(compartments, len(line)-1)):
        char1, char2 = line[pos1], line[pos2]
        sack1.add(char1)
        sack2.add(char2)
        for char in (char1, char2):
            if char in sack1 and char in sack2:
                pri = priority(char)
                if opts.verbose:
                    print(f"{char} -> priority {pri}")
                return pri

def main(stream, opts):
    prisum = 0
    for line in stream:
        prisum += correct_sack(line, opts)
    print("part 1:", prisum)
