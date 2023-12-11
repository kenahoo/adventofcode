# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal;
import math
import re

directions = {
    '|': [(-1, 0), (1, 0)],
    '-': [(0, -1), (0, 1)],
    'L': [(-1, 0), (0, 1)],
    'J': [(-1, 0), (0, -1)],
    '7': [(1, 0), (0, -1)],
    'F': [(1, 0), (0, 1)],
    '.': [],
    'S': [(-1, 0), (1, 0)],  # By inspection, S is a "|"
}


with open('data/10') as fh:
    grid = fh.readlines()

# Distances from S to each point
dists = [[math.inf] * len(grid[0]) for _ in grid]

# Position of S
s_loc = None
for i, line in enumerate(grid):
    if 'S' in line:
        s_loc = (i, line.index('S'))
        break


def global_max(dists):
    return max([max(-1 if d_==math.inf else d_  for d_ in d) for d in dists])


def can_move(location, direction):
    a, b = direction
    i_, j_ = location[0] + a, location[1] + b
    try:
        new_char = grid[i_][j_]
    except IndexError:
        return False
    back = (a * -1, b * -1)
    return back in directions[new_char]


stack = [s_loc]
dists[s_loc[0]][s_loc[1]] = 0

while stack:
    i, j = stack.pop()
    for dir in directions[grid[i][j]]:
        if can_move([i, j], dir):
            i_, j_ = [i + dir[0], j + dir[1]]
            if dists[i][j] + 1 < dists[i_][j_]:
                dists[i_][j_] = dists[i][j] + 1
                stack.append([i_, j_])

print(global_max(dists))
