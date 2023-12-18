import re
from itertools import pairwise

import numpy as np

direction = {  # Directions
    'r': np.array([0, 1]),
    'l': np.array([0, -1]),
    'u': np.array([-1, 0]),
    'd': np.array([1, 0]),
}


def shoelace_area(path):  # Path should already be closed
    # Use Shoelace Formula to find total area inside the path
    return round(abs(sum([np.linalg.det(np.c_[p1, p2]) for p1, p2 in pairwise(path)])) / 2)


def main(file):
    pos = np.array([0, 0])
    path = [pos]
    path_len = 0

    with open(file) as fh:
        for line in fh.readlines():
            m = re.match(r'(\w) (\d+)', line)
            d, l = m.group(1).lower(), int(m.group(2))

            pos = pos + direction[d] * l
            path.append(pos)
            path_len += l

    print(shoelace_area(path) + path_len/2 + 1)


main('data/18')
# main('/tmp/example')
