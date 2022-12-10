from collections import defaultdict

def crt_cycle(cc, crtbuf, X, sigstrength, opts):
    if cc == 19 or (cc + 1 - 20) % 40 == 0:
        if opts.verbose:
            print(f"cc {cc}: X is {X}: sigstrength += {(cc+1)*X}")
        sigstrength += (cc + 1) * X
        if opts.verbose:
            print(f"  ... = {sigstrength}")

    col = cc % 40
    row = cc // 40
    if X - 1 <= col <= X + 1:
        crtbuf[row][col] = "#"

    if opts.verbose and col == 0 and row > 0:
        print(f"finished row {row-1}:")
        print("".join(crtbuf[row-1]))

    return sigstrength

def main(stream, opts):
    X = 1
    cc = 0

    crtbuf = [list("." * 40) for _ in range(6)]
    sigstrength = 0
    for insn in stream:
        if insn.startswith("addx"):
            for cc in range(cc, cc + 2):
                sigstrength = crt_cycle(cc, crtbuf, X, sigstrength, opts)
            X += int(insn[5:-1])
        else: # noop
            sigstrength = crt_cycle(cc, crtbuf, X, sigstrength, opts)

        cc += 1

    print("part 1:", sigstrength, "after", cc, "cycles")
    print("part 2:")
    print("\n".join("".join(line) for line in crtbuf))
