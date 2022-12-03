# ROCK: 0
# PAPER: 1
# SCISSORS: 2

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

def score_round(me, opp, opts, is_goal=False):
    opp_choice = ord(opp) - ord("A")
    if not is_goal:
        me_choice = ord(me) - ord("X")
        diff = me_choice - opp_choice
    else:
        diff = ord(me) - ord("X") - 1 # 0 -> lose; 1 -> draw; 2 -> win
        me_choice = (opp_choice + diff) % 3
    score = SCORES[diff] + me_choice + 1
    if opts and opts.verbose:
        print(
            f"{line.strip()} -> {NAMES[me]} vs. {NAMES[opp]} -> {SCORES[diff]}"
            f" + {me_choice} = {score}"
        )
    return score

def run_game(lines, opts, is_goal=False):
    score = 0
    for line in lines:
        score += score_round(line[2], line[0], opts, is_goal=is_goal)
    return score

def main(stream, opts=None):
    lines = stream.readlines()
    print("part 1 score:", run_game(lines, opts, False))
    print("part 2 score:", run_game(lines, opts, True))

