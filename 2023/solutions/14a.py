def main(file):
    with open(file) as fh:
        a = [x.rstrip() for x in fh.readlines()]
        # a = np.array([[*x.rstrip()] for x in fh.readlines()]).transpose()

    transposed = transpose(a)
    # transposed = "\n".join(''.join(x) for x in a)

    print(transposed)
    print("\n")

    # Shift left
    shifted = [shift_left(x) for x in transposed]
    print(shifted)
    print("\n")

    i = 1
    weight = 0
    for row in reversed(transpose(shifted)):
        weight += i * row.count('O')
        i += 1

    print(weight)


def shift_left(x: str):
    while True:
        new = x.replace(r".O", "O.")
        if new == x:
            return new
        x = new


def transpose(a: list[str]) -> list[str]:
    return [''.join(a[i][j] for i in range(len(a))) for j in range(len(a[0]))]


main('/tmp/example')
