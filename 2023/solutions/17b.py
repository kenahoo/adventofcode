from dataclasses import dataclass

import numpy as np

direction = {  # Directions
    'r': (0, 1),
    'l': (0, -1),
    'u': (-1, 0),
    'd': (1, 0),
}

opposite = {
    'r': 'l',
    'l': 'r',
    'u': 'd',
    'd': 'u',
}


@dataclass
class State:
    i: int
    j: int
    d: str  # Direction
    streak: int
    cost: int

    def __repr__(self):
        return f"[{self.i}, {self.j}] {self.d}[{self.streak}]: {self.cost}"

    def __hash__(self):
        return hash((self.i, self.j, self.d, self.streak))

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j and self.d == other.d and self.streak == other.streak


def main(file):
    with open(file) as fh:
        a = [[int(y) for y in x.rstrip()] for x in fh.readlines()]
    print(f"Grid size is {len(a)} x {len(a[0])} = {len(a) * len(a[0])}")

    # For each position x, y, array holds map of [how we got there, min distance]
    mins = [[dict() for _ in range(len(a[0]))] for _ in range(len(a))]

    # Pretend we start by moving right, but streak is 0, so it doesn't count against us
    stack = {State(0, 0, 'r', 0, 0)}
    mins[0][0] = {('r', 0): 0, ('d', 0): 0}  # position, direction, streak, cost
    while stack:
        s = stack.pop()
        for next_d in 'drul':
            if len(stack) % 10000 == 0:
                # Max distinct states should be 141 * 141 * 4 * 3 = 238572
                print(f"Stack size is {len(stack)}")
            if next_d == opposite[s.d]:
                # Can't go back
                continue

            if next_d == s.d:
                if s.streak == 10:
                    # Can't continue this way
                    continue
                moves = [1]
                next_streak = s.streak + 1
            else:
                # Different direction, we need to go at least 4 spaces in this new direction
                moves = [1, 2, 3, 4]
                next_streak = 4

            new_i, new_j = s.i + moves[-1]*direction[next_d][0], s.j + moves[-1]*direction[next_d][1]
            if new_i < 0 or new_i >= len(a) or new_j < 0 or new_j >= len(a[0]):  # Off the board
                continue
            vec = direction[next_d]
            cur_cost = mins[s.i][s.j][(s.d, s.streak)]

            next_cell = mins[new_i][new_j]
            next_cost = cur_cost + sum(a[s.i + vec[0] * i][s.j + vec[1] * i] for i in moves)

            add = True
            for i in range(10):
                # Don't add if we're beaten on both cost & streak for this direction
                if next_cell.get((next_d, next_streak - i), np.inf) <= next_cost:
                    add = False
            if add:
                next_cell[(next_d, next_streak)] = next_cost
                stack.add(State(new_i, new_j, next_d, next_streak, next_cost))

    print(min(mins[-1][-1].values()))


main('data/17')
# main('/tmp/example')
