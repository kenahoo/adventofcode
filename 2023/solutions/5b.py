import re


class Ival:
    def __init__(self, low, high, target=None):
        self.low = low
        self.high = high
        self.target = target

    def __contains__(self, item):
        return self.low <= item <= self.high

    def __repr__(self):
        return f"[{self.low}, {self.high}] -> {self.target}"

    def overlaps(self, other):
        return self.low <= other.high and other.low <= self.high

    def map(self, seed):
        return seed - self.low + self.target

    def map_ival(self, other):
        if other.low in self and other.high in self:
            return [Ival(self.map(other.low), self.map(other.high), None)]
        if other.low < self.low:
            return []


class Ivals:
    def __init__(self):
        self.ivals: list[Ival] = []

    def __repr__(self):
        return "\n".join([str(x) for x in self.ivals])

    def add(self, low, high, target):
        self.ivals.append(Ival(low, high, target))
        self.ivals = sorted(self.ivals, key=lambda x: x.low)  # Keep 'em sorted

    def disjoint(self):
        for i in range(len(self.ivals) - 1):
            if self.ivals[i].overlaps(self.ivals[i + 1]):
                return False
        return True

    def map_ival(self, other: Ival):
        for iv in self.ivals:
            if other.overlaps(iv):
                if other.low < iv.low:
                    return [Ival(other.low, iv.low - 1),
                            *self.map_ival(Ival(iv.low, other.high))]
                if other.high <= iv.high:
                    return [iv.map(Ival(other.low, other.high))]
                return [iv.map(Ival(other.low, iv.high)),
                        *self.map_ival(Ival(iv.high + 1, other.high))]

        return [other]


class IvalsStack:
    def __init__(self, ivalses: list[Ivals] = None):
        self.ivalses: ivalses or []

    def map_ival(self, other: Ival):
        for ivals in self.ivalses:
            ivals.map_ival(other)


# Construct all the mappings
def get_mappings(data):
    maps = re.findall(r'\w+-to-\w+ map:((?:\s+\d+)+)', data)
    for i in range(len(maps)):
        ivals = Ivals()
        for x, y, z in re.findall(r'(\d+) (\d+) (\d+)', maps[i]):
            ivals.add(int(y), int(y) + int(z) - 1, int(x))
        if not ivals.disjoint():
            raise ValueError(f"Not disjoint {i}")

        maps[i] = ivals
    return maps


# Find all the seed ranges
def get_seeds(data):
    m = re.search(r'seeds: [\d ]+', data)
    seed_str = m.group(0)
    return [Ival(int(x[0]), int(x[1])) for x in re.findall(r'(\d+) (\d+)', seed_str)]


with open('data/5') as fh:
    data = fh.read()

maps = get_mappings(data)
seeds = get_seeds(data)

lowest = 1e20
while seeds:
    seed = seeds.pop(0)
    for map in maps:
        result = map.map_ival(seed)

print(seeds)

