from collections import deque

def find_marker(string, marker_len):
    nunique = 0
    nelem = 0
    bufset = [0] * 26 # a - z
    char = None
    for index in range(marker_len, len(string)):
        if nelem == marker_len:
            oldchar = ord(string[index-marker_len]) - ord('a')
            bufset[oldchar] -= 1
            nelem -= 1
            if bufset[oldchar] == 0:
                nunique -= 1
        char = ord(string[index]) - ord('a')
        if not bufset[char]:
            nunique += 1
        bufset[char] += 1
        nelem += 1
        if nelem == marker_len and nunique == marker_len:
            return index
    return -1

def main(stream, opts):
    string = stream.read().strip()
    print("part 1:", find_marker(string, 4) + 1)
    print("part 2:", find_marker(string, 14) + 1)
