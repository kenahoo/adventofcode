
direction = {
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1),
    '^': (-1, 0),
}


def main(file):
    with open(file) as fh:
        a = [line.rstrip() for line in fh.readlines()]

    start = (0, 1)
    end = (len(a) - 1, len(a[-1]) - 2)

    lengths = []
    paths = [(*start, {(0, 0)})]
    while paths:
        row, col, seen = paths.pop(0)

        for dir, ij in direction.items():
            i, j = ij
            new_row, new_col = row + i, col + j
            new_char = a[new_row][new_col]

            if not (0 <= new_row < len(a)) or not (0 <= new_col < len(a[new_row])):
                continue
            if (new_row, new_col) in seen:
                continue

            if new_char == '#':
                continue
            if new_char == '.':  # Can go this way
                if (new_row, new_col) == end:
                    lengths.append(len(seen))
                else:
                    paths.append((new_row, new_col, seen | {(new_row, new_col)}))

            if new_char in direction.keys():
                if ij != direction[new_char]:  # Direction mismatch
                    continue
                paths.append((new_row, new_col, seen | {(new_row, new_col)}))

    print(lengths)


main('data/23')
# main('/tmp/example')
