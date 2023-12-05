import logging
import re


class Ival:
    """A single interval, with a target value that tells how to map values"""
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

    def _map(self, num):
        return num - self.low + self.target

    def map_ival(self, other):
        # 'other' must be contained in 'self'
        if other.low < self.low or other.high > self.high:
            raise ValueError(f"Can't map {other} to {self}")
        return [Ival(self._map(other.low), self._map(other.high), None)]


class Ivals:
    """A collection of intervals that can map values"""
    def __init__(self):
        self.ivals: list[Ival] = []

    def __repr__(self):
        return "\n".join([str(x) for x in self.ivals])

    def add(self, low, high, target):
        self.ivals.append(Ival(low, high, target))
        self.ivals = sorted(self.ivals, key=lambda x: x.low)  # Keep 'em sorted

    def disjoint(self):
        """Check whether all these intervals are disjoint - lucky for us, all the x-to-y maps are."""
        for i in range(len(self.ivals) - 1):
            if self.ivals[i].overlaps(self.ivals[i + 1]):
                return False
        return True

    def map_ival(self, other: Ival) -> list[Ival]:
        """Map 'other' through all the regions (intervals and areas outside intervals) it overlaps with"""
        for iv in self.ivals:
            if other.overlaps(iv):
                if other.low < iv.low:
                    return [Ival(other.low, iv.low - 1),
                            *self.map_ival(Ival(iv.low, other.high))]
                if other.high <= iv.high:
                    return iv.map_ival(Ival(other.low, other.high))
                return [*iv.map_ival(Ival(other.low, iv.high)),
                        *self.map_ival(Ival(iv.high + 1, other.high))]

        return [other]


def get_mappings(data):
    """Construct all the mappings"""
    maps = re.findall(r'\w+-to-\w+ map:((?:\s+\d+)+)', data)
    for i in range(len(maps)):
        ivals = Ivals()
        for x, y, z in re.findall(r'(\d+) (\d+) (\d+)', maps[i]):
            ivals.add(int(y), int(y) + int(z) - 1, int(x))
        if not ivals.disjoint():
            raise ValueError(f"Not disjoint {i}")

        maps[i] = ivals
    return maps


def get_seeds(data):
    """Find all the seed ranges"""
    m = re.search(r'seeds: [\d ]+', data)
    seed_str = m.group(0)
    return [Ival(int(x[0]), int(x[1])+int(x[0])-1) for x in re.findall(r'(\d+) (\d+)', seed_str)]


def main():
    logging.getLogger().setLevel(logging.WARNING)

    with open('data/5') as fh:
        data = fh.read()

    maps = get_mappings(data)
    seeds = get_seeds(data)

    for m in maps:
        logging.info(f"Mapping:\n{m}")
        mapped = []
        for seed in seeds:
            logging.info(f"Seed:{seed}")
            result = m.map_ival(seed)
            logging.info(f"Result:{result}")
            mapped += result
        seeds = mapped

    print(min(seed.low for seed in seeds))


main()
