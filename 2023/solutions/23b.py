import re

direction = {
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1),
    '^': (-1, 0),
}


def find_junctions(a):
    junctions = []
    for i in range(1, len(a)-1):
        for j in range(1, len(a[i])-1):
            if a[i][j] != '.':
                continue
            dirs = sum(a[i+c][j+d] == '.' for c, d in direction.values())
            if dirs > 2:
                print(i)
                junctions.append([i, j])
    return junctions


def main(file):
    with open(file) as fh:
        a = [re.sub('[<>^v]', '.', line.rstrip()) for line in fh.readlines()]

    jc = find_junctions(a)

    start = (0, 1)
    end = (len(a) - 1, len(a[-1]) - 2)

    lengths = []
    paths = [(*start, {(0, 0)})]
    prev_paths = 0
    while paths:
        if len(paths) != prev_paths:
            print(f"{len(paths)} paths")
        prev_paths = len(paths)
        row, col, seen = paths.pop(0)

        to_add = []
        for dir, ij in direction.items():
            new_row, new_col = row + ij[0], col + ij[1]
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
                    to_add.append((new_row, new_col))

        if len(to_add) == 1:
            # Don't allocate new set
            new_row, new_col = to_add[0]
            seen.add((new_row, new_col))
            paths.append((new_row, new_col, seen))
        elif len(to_add) > 1:
            for new_row, new_col in to_add:
                paths.append((new_row, new_col, seen | {(new_row, new_col)}))

    print(lengths)


main('data/23')
# main('/tmp/example')
