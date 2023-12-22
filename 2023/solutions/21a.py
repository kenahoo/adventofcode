def try_step(a, rc, out: set):
    r, c = rc
    if 0 <= r < len(a) and 0 <= c < len(a[0]) and a[r][c] != '#':
        out.add(rc)


def take_steps(a, rc):
    out = set()
    for row, col in rc:
        try_step(a, (row - 1, col), out)
        try_step(a, (row + 1, col), out)
        try_step(a, (row, col - 1), out)
        try_step(a, (row, col + 1), out)
    return out


def main(file):

    with open(file) as fh:
        a = [x.rstrip() for x in fh.readlines()]

    r = [i for i, x in enumerate(a) if 'S' in x]
    c = [a[r[0]].index('S')]
    rc = zip(r, c)

    for i in range(64):
        rc = take_steps(a, rc)

    print(len(rc))


main('data/21')
# main('/tmp/example')
