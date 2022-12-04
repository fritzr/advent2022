import time

def main(stream, opts=None):
    start = time.time()
    calories = sorted(
        sum(int(line.strip()) for line in section.split("\n") if line.strip())
        for section in stream.read().split("\n\n")
    )
    print("part 1:", calories[-1])
    top3 = calories[-3:]
    print("part 2:", " + ".join(map(str, top3)), "=", sum(top3))
    if opts.time:
        print("time:", time.time() - start)
