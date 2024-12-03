def try_step(a, rc, out: set):
    r, c = rc
    if 0 <= r < len(a) and 0 <= c < len(a[0]) and a[r][c] != '#':
        out.add(rc)


def take_steps(a, rc):
    # n = len(a)
    out = set()
    for row, col in rc:
        try_step(a, ((row - 1), col), out)
        try_step(a, ((row + 1), col), out)
        try_step(a, (row, (col - 1)), out)
        try_step(a, (row, (col + 1)), out)
    return out


def view(a, rc):
    n = len(a)
    out = ''
    for i in range(n):
        out += ' '
        for j in range(n):
            out += 'O' if (i, j) in rc else a[i][j]
        out += "\n"
    print(out)


def saturate(a, start):
    num_open = sum([1 for row in a for x in row if x != '#'])
    print(f"Starting at {start}, num open: {num_open}")

    seen = {}
    i = 1
    rc = start

    while True:
        hash_ = ','.join(str(x) for x in rc)
        if hash_ in seen:
            result, j = seen[hash_]
            print(f'loop detected at step {i} with {len(result)} occupied spots, first seen at {j}')
            # break
        else:
            result = take_steps(a, rc)
        # if len(result) == num_open:
        #     print(f"Saturated after {i} steps")
        #     return i
            seen[hash_] = [result, i]
        # view(a, result)
        rc = result
        i += 1


def main(file):
    with open(file) as fh:
        a = [x.rstrip() for x in fh.readlines()]

    n = len(a)

    # Find the starting 'S'
    start_r = [i for i, x in enumerate(a) if 'S' in x]
    start_c = [a[start_r[0]].index('S')]
    start = tuple(zip(start_r, start_c))


    # open_cells = 0
    # for i in range(len(a)):
    #     for j in range(len(a[i])):
    #         if (i + j - steps) % 2 == 0 and a[i][j] == '.':
    #         # if (i - steps) % 2 == 1 and (j - steps) % 2 == 1 and a[i][j] == '.':
    #             open_cells += 1
    #
    # print(open_cells)


    steps = 26501365

    # For the example data set:
    # Starting in upper left corner: 20 steps to saturation (42), 21 to (39)
    # Starting in upper right corner: 21 steps to saturation (39), 22 to (42)
    # Starting in lower left corner: 20 steps to saturation (42), 21 to (39)
    # Starting in lower right corner: 20 steps to saturation (42), 21 to (39)
    # Starting at left: 19 steps to saturation (42), 20 to (39)
    # Starting at top: 20 steps to saturation (39), 21 to (42)
    # Starting at right: 18 steps to saturation (39), 19 to (42)
    # Starting at bottom: 20 steps to saturation (39), 21 to (42)
    start = {(len(a)-1, (len(a)-1)>>1)}
    saturate(a, start)

    seen = {}
    for i in range(steps):
        hash_ = ','.join([str(x) for x in start])
        if hash_ in seen:
            result, j = seen[hash_]
            print(f'loop detected at {i} with {len(result)} at {j}')
            # break
        else:
            result = take_steps(a, start)
            seen[hash_] = [result, i]
        start = result
        if i % 1000 == 0:
            print(i)

    print(len(start))


# main('data/21')
main('/tmp/example')
