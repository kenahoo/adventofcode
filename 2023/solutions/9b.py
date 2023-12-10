import re
from itertools import pairwise


def inputs(file):
    out = []
    with open(file) as fh:
        for line in fh.readlines():
            out.append(list(int(x) for x in re.findall(r'[-\d]+', line)))
    return out


def diff(seq: list[int]) -> list[int]:
    return [y - x for x, y in pairwise(seq)]


def extend(seq: list[int]) -> list[int]:
    if all(x == 0 for x in seq):
        return [0, *seq]

    d = extend(diff(seq))
    return [seq[0] - d[0], *seq]


def main(file):
    tot = 0
    for num in inputs(file):
        tot += extend(num)[0]
    print(tot)


main('data/9')
# main('/tmp/example')
