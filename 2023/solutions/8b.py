import re
from math import lcm


def inputs(file):
    trans = {}
    with open(file) as fh:
        lrs = fh.readline().strip()
        for line in fh.readlines():
            if re.match(r'^$', line):
                continue
            m = re.match(r'(\w+) = \((\w+), (\w+)\)', line)
            trans[m.group(1)] = {'L': m.group(2), 'R': m.group(3)}
    return lrs, trans


def cycle_len(cur, lrs, trans):
    i = j = 0
    while True:
        cur = trans[cur][lrs[j]]
        if cur[2] == 'Z':
            return i+1
        i += 1
        j = (j + 1) % len(lrs)


def main(file):
    lrs, trans = inputs(file)

    lengths = [cycle_len(x, lrs, trans) for x in trans if x[2] == 'A']
    print(lcm(*lengths))


main('data/8')
# main('/tmp/example3')
