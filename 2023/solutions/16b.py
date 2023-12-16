import copy

direction = {  # Directions
    'r': (0, 1),
    'l': (0, -1),
    'u': (-1, 0),
    'd': (1, 0),
}


def go(x):
    return *direction[x], x


transitions = {
    # First character: which way we're currently moving
    # Second character: what we see at the current location
    'r.': [go('r')],
    'r|': [go('u'), go('d')],
    'r-': [go('r')],
    'r/': [go('u')],
    'r\\': [go('d')],

    'l.': [go('l')],
    'l|': [go('u'), go('d')],
    'l-': [go('l')],
    'l/': [go('d')],
    'l\\': [go('u')],

    'u.': [go('u')],
    'u|': [go('u')],
    'u-': [go('l'), go('r')],
    'u/': [go('r')],
    'u\\': [go('l')],

    'd.': [go('d')],
    'd|': [go('d')],
    'd-': [go('l'), go('r')],
    'd/': [go('l')],
    'd\\': [go('r')],
}


def show(a, x, y):
    a = copy.deepcopy(a)
    # Replace the current location with a *
    a[x] = a[x][:y] + '*' + a[x][y + 1:]
    print('\n'.join(a))


def main(file):
    with open(file) as fh:
        a = [x.rstrip() for x in fh.readlines()]

    rows = len(a)
    cols = len(a[0])

    starts = ([(i, 0, 'r') for i in range(rows)] +
              [(0, i, 'd') for i in range(cols)] +
              [(i, rows - 1, 'l') for i in range(rows)] +
              [(cols - 1, i, 'u') for i in range(cols)])

    print(max([num_lit(a, *start) for start in starts]))


def num_lit(a, start_x, start_y, start_dir):
    seen = set()
    beams = [(start_x, start_y, start_dir)]
    while beams:
        new_beams = []
        for x, y, dir in beams:
            seen.add((x, y, dir))
            for vector_x, vector_y, dir_ in transitions[dir + a[x][y]]:
                new_x, new_y = x + vector_x, y + vector_y
                if 0 <= new_x < len(a) and 0 <= new_y < len(a[0]) and (new_x, new_y, dir_) not in seen:
                    new_beams.append((new_x, new_y, dir_))
        beams = new_beams
    seen_locs = {(x, y) for x, y, _ in seen}
    return len(seen_locs)


main('data/16')
