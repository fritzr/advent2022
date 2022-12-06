from collections import deque

def find_marker(string, marker_len):
    buffer = deque(string[:marker_len])
    for index in range(marker_len, len(string)):
        buffer.popleft()
        buffer.append(string[index])
        if len(set(buffer)) == len(buffer):
            return index
    return -1

def main(stream, opts):
    string = stream.read()
    print("part 1:", find_marker(string, 4) + 1)
    print("part 2:", find_marker(string, 14) + 1)
