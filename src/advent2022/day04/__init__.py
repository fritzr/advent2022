
def contains(range1, range2):
    assert(range1[0] <= range1[1] and range2[0] <= range2[1])
    return range1[0] >= range2[0] and range1[1] <= range2[1]

def main(stream, opts):
    containments = 0
    for line in stream:
        elves = line.strip().split(",")
        assert(len(elves) == 2)
        rooms = [
            tuple(int(endpoint) for endpoint in room_range.split("-"))
            for room_range in elves
        ]
        for index in range(len(rooms)):
            if contains(rooms[index], rooms[index-1]):
                containments += 1
                break


    print("part 1:", containments)
