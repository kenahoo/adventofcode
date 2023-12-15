class Map:
    def __init__(self, a: list[str]):
        self.a: list[str] = a
        self.turned = 0

    def __repr__(self):
        # Just for looking at it
        return "\n".join(''.join(x) for x in self.a)

    def show(self, original=False):
        # Just for looking at it
        if original:
            # Original orientation
            b = type(self)(self.a.copy())
            for i in range(4 - (self.turned % 4)):
                b.rotate_clockwise()
            print(repr(b) + "\n")
        else:
            print(repr(self) + "\n")

    def rotate_clockwise(self):
        self.a = [''.join(self.a[i][j] for i in reversed(range(len(self.a)))) for j in range(len(self.a[0]))]
        self.turned += 1

    @classmethod
    def _shift_right(cls, x: str):
        while True:
            new = x.replace(r"O.", ".O")
            if new == x:
                return new
            x = new

    def shift_all_right(self):
        self.a = [self._shift_right(x) for x in self.a]

    def weight(self):
        i = 1
        weight = 0
        for row in reversed(self.a):
            weight += i * row.count('O')
            i += 1
        return weight


def main(file):
    with open(file) as fh:
        a = Map([x.rstrip() for x in fh.readlines()])

    period = None
    results = {}
    for i in range(1, 1000000000):
        step(a)
        step(a)
        step(a)
        step(a)

        if repr(a) in results:
            j = results[repr(a)][0]
            period = i - j
            print(f"Result {i} is the same as result {j}, period is {period}")

        if period is not None and i % period == 1000000000 % period:
            print(f"\nAnswer: {a.weight()}")
            break

        results[repr(a)] = [i, a.weight()]


def step(a):
    a.rotate_clockwise()
    a.shift_all_right()


main('data/14')
