# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal;
import math
from itertools import pairwise
from time import sleep

# import numpy as np

directions = {
    '|': [(-1, 0), (1, 0)],
    '-': [(0, -1), (0, 1)],
    'L': [(-1, 0), (0, 1)],
    'J': [(-1, 0), (0, -1)],
    '7': [(1, 0), (0, -1)],
    'F': [(1, 0), (0, 1)],
    '.': [],
}
s_is = '|'  # By inspection, S is a "|"
directions['S'] = directions[s_is]

# Unicode box drawing characters
draw = {
    '|': '│',
    '-': '─',
    'L': '└',
    'J': '┘',
    '7': '┐',
    'F': '┌',
}


def global_max(dists):
    # Find the max non-infinite value in the grid
    return max([max(-1 if d_ == math.inf else d_ for d_ in d) for d in dists])


def can_move(location, direction, grid):
    a, b = direction
    i_, j_ = location[0] + a, location[1] + b
    try:
        new_char = grid[i_][j_]
    except IndexError:
        return False
    back = (a * -1, b * -1)
    return back in directions[new_char]


def path_to_max(dists, start, grid):
    path = []
    udlr = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    cur = start
    while True:
        path.append(cur)
        for k in udlr:
            new_point = [cur[0] + k[0], cur[1] + k[1]]
            try:
                if dists[new_point[0]][new_point[1]] == dists[cur[0]][cur[1]] + 1 and can_move(cur, k, grid):
                    cur = new_point
                    break
            except IndexError:
                pass  # We're off the grid
        else:
            # We didn't find a new point
            return path


def show(grid, pos=None):
    if pos:
        grid = [*grid]
        # Replace the character at pos with a *
        grid[pos[0]] = grid[pos[0]][:pos[1]] + '*' + grid[pos[0]][pos[1]+1:]
        # grid[pos[0]][pos[1]] = '*'
    trans = str.maketrans(draw)
    for g in grid:
        print(g.rstrip().translate(trans))


def main(file):
    with open(file) as fh:
        grid = fh.readlines()

    # Distances from S to each point
    dists = [[math.inf] * len(grid[0]) for _ in grid]

    # Position of S
    s_loc = [[i, j] for i in range(len(grid)) for j in range(len(grid[i])) if grid[i][j] == 'S'][0]

    stack = [s_loc]
    dists[s_loc[0]][s_loc[1]] = 0
    while stack:
        i, j = stack.pop()
        for dir in directions[grid[i][j]]:
            if can_move([i, j], dir, grid):
                i_, j_ = [i + dir[0], j + dir[1]]
                if dists[i][j] + 1 < dists[i_][j_]:
                    dists[i_][j_] = dists[i][j] + 1
                    stack.append([i_, j_])

    # Retrace steps to find path
    path1 = path_to_max(dists, [s_loc[0] + directions['S'][0][0], s_loc[1] + directions['S'][0][1]], grid)
    path2 = path_to_max(dists, [s_loc[0] + directions['S'][1][0], s_loc[1] + directions['S'][1][1]], grid)
    path = [s_loc] + path1 + path2[:-1][::-1]

    show(grid)
    # Animate the path
    # for p in path:
    #     show(grid, p)
    #     sleep(1)

    area = shoelace_area(path)

    print(area - len(path)/2 + 1)


def shoelace_area(path):
    # Use Shoelace Formula to find total area inside the path
    path = [*path, path[0]]
    return abs(sum([p1[0] * p2[1] - p1[1] * p2[0] for p1, p2 in pairwise(path)])) / 2


main('data/10')
