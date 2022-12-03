# ROCK: A X
# PAPER: B Y
# SCISSORS: C Z

SCORES = [
    3, # draw: diff == 0
    6, # win: diff == 2
    0, # lose: diff == 1
]

NAMES = {
    "A": "rock", "X": "rock",
    "B": "paper", "Y": "paper",
    "C": "scissors", "Z": "scissors",
}

def score_round(me, opp, opts):
    opp_choice = ord(opp) - ord("A")
    me_choice = ord(me) - ord("X")
    diff = me_choice - opp_choice
    score = SCORES[diff] + me_choice + 1
    if opts and opts.verbose:
        print(
            f"{line.strip()} -> {NAMES[me]} vs. {NAMES[opp]} -> {SCORES[diff]}"
            f" + {me_choice} = {score}"
        )
    return score

def part1(lines, opts):
    score = 0
    for line in lines:
        score += score_round(line[2], line[0], opts)
    return score

def part2(lines, opts):
    score = 0
    for line in lines:
        opponent = ord(line[0]) - ord("A")
        me = ord(line[2]) - ord("X")
        diff = me - opponent
        this_score = SCORES[diff] + me + 1
        if opts and opts.verbose:
            print(
                line.strip(),
                "->",
                NAMES[line[2]],
                "vs.",
                NAMES[line[0]],
                "->",
                SCORES[diff],
                "+",
                me,
                "=",
                this_score,
            )
        score += this_score
    return score


def main(stream, opts=None):
    lines = stream.readlines()
    print("part 1 score:", part1(lines, opts))

