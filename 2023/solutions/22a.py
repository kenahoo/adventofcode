import re
from collections import defaultdict

import numpy as np


def expand(brick):
    x, y, z, x_, y_, z_ = map(int, re.match(r'(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)', brick).groups())
    if x == x_ and y == y_:
        return [[x, y, i] for i in range(int(z), int(z_) + 1)]
    if x == x_ and z == z_:
        return [[x, i, z] for i in range(int(y), int(y_) + 1)]
    return [[i, y, z] for i in range(int(x), int(x_) + 1)]


def supported_by(brick, occupied: np.array):
    out = set()
    for x, y, z in brick:
        i = occupied[x, y, z]
        if occupied[x, y, z - 1] not in (i, 0):
            out.add(occupied[x, y, z - 1])
    return out


def can_move_down(brick, i, occupied):
    for x, y, z in brick:
        if z == 1 or (occupied[x, y, z - 1] not in (i, 0)):
            return False
    return True


def move_down(brick, i, occupied):
    for x, y, z in brick:
        occupied[x, y, z - 1] = i
        occupied[x, y, z] = 0
    for square in brick:
        square[2] -= 1


def main(file):
    with open(file) as fh:
        a = [expand(line) for line in fh.readlines()]

    max_x = max([max([x for x, _, _ in brick]) for brick in a])
    max_y = max([max([y for _, y, _ in brick]) for brick in a])
    max_z = max([max([z for _, _, z in brick]) for brick in a])

    occupied = np.zeros((max_x+1, max_y+1, max_z+1), dtype=np.int_)

    for i, brick in enumerate(a):
        for square in brick:
            occupied[tuple(square)] = i + 1

    while True:
        moved = False
        for i, brick in enumerate(a):
            if can_move_down(brick, i+1, occupied):
                print(f"Moving {i+1} {brick} down: ", end='')
                move_down(brick, i+1, occupied)
                print(f"{brick}")
                moved = True
                break
        if not moved:
            break

    print("Bricks:")
    for i, brick in enumerate(a):
        print(f"Brick {i+1}: {brick}")

    supported_by_ = {i + 1: supported_by(brick, occupied) for i, brick in enumerate(a)}
    supports = defaultdict(set)
    for i, spb in supported_by_.items():
        for j in spb:
            supports[j].add(i)

    print(f"supports: {supports}")
    print(f"supported_by: {supported_by_}")

    free = 0
    for i, brick in enumerate(a):
        for upper_brick in supports[i+1]:
            if len(supported_by_[upper_brick]) == 1:
                print(f"Brick {i+1} is the only supporter of {upper_brick}")
                break
        else:
            print(f"Brick {i+1} looks free")
            free += 1

    # print(a)
    print(free)


main('data/22')
# main('/tmp/example')
