import numpy as np


def slice(a, i, j):
    return a[i:j] if i < j else a[j:i]


def main(file, expander=2):
    with open(file) as fh:
        a = np.array([[*x.rstrip()] for x in fh.readlines()])

    blank_rows = np.all(a == '.', axis=1)
    blank_cols = np.all(a == '.', axis=0)

    galaxies = np.argwhere(a == '#')

    total_dists = 0
    for i in range(len(galaxies)):
        g_i = galaxies[i]
        for j in range(i + 1, len(galaxies)):
            g_j = galaxies[j]
            if blank_rows[g_i[0]] or blank_rows[g_j[0]]:
                raise Exception(f"blank row {g_i[0]}")
            if blank_cols[g_i[1]] or blank_cols[g_j[1]]:
                raise Exception(f"blank col {g_i[0]}")
            extra_x = sum(slice(blank_rows, g_i[0], g_j[0]))
            extra_y = sum(slice(blank_cols, g_i[1], g_j[1]))
            dist = sum(abs(g_i - g_j)) + (expander-1)*(extra_x + extra_y)
            # print(f"{i};{g_i} -> {j};{g_j} = {dist}")
            total_dists += dist

    print(total_dists)


main('data/11')
main('data/11', 1e6)
