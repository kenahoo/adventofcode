import re
from itertools import pairwise

import numpy as np

direction = {  # Directions
    'r': np.array([0, 1]),
    'd': np.array([1, 0]),
    'l': np.array([0, -1]),
    'u': np.array([-1, 0]),
}
dir_codes = ''.join(direction.keys())


def shoelace_area(path):  # Path should already be closed
    # Use Shoelace Formula to find total area inside the path
    return round(abs(sum([np.linalg.det(np.c_[p1, p2]) for p1, p2 in pairwise(path)])) / 2)


def main(file):
    path = [np.array([0, 0])]
    path_len = 0

    with open(file) as fh:
        for line in fh.readlines():
            len_, dir = re.search(r'#([\dabcdef]{5})(\d)', line).groups()
            len_ = int(len_, 16)
            path.append(path[-1] + direction[dir_codes[int(dir)]] * len_)
            path_len += len_

    print(shoelace_area(path) + path_len/2 + 1)


main('data/18')
# main('/tmp/example')
