from operator import mul
from functools import reduce

def scenic_score(forest, row, col, opts):
    viewable = False
    visible = [0, 0, 0, 0] # left, right, above, below
    for dir_id, colrange in enumerate((range(col-1, -1, -1), range(col+1, len(forest[row])))):
        for ocol in colrange:
            visible[dir_id] += 1
            if forest[row][ocol] >= forest[row][col]:
                break
        else:
            viewable = True
    for dir_id, rowrange in enumerate((range(row-1, -1, -1), range(row+1, len(forest)))):
        for orow in rowrange:
            visible[dir_id + 2] += 1
            if forest[orow][col] >= forest[row][col]:
                break
        else:
            viewable = True
    return viewable, reduce(mul, visible)

def main(stream, opts):
    forest = [line[:-1] for line in stream.readlines()]

    nvisible = 0
    best_view = 0
    best_loc = (-1, -1)
    for row in range(len(forest)):
        for col in range(len(forest[0])):
            viewable, score = scenic_score(forest, row, col, opts)
            if viewable:
                nvisible += 1
            if score > best_view:
                best_view = score
                best_loc = (row, col)

    print("part 1:", nvisible)
    print("part 2:", best_view, "from", best_loc, "=", forest[best_loc[0]][best_loc[1]])

