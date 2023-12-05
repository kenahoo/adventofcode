import re

with open('data/5') as fh:
    data = fh.read()

m = re.search(r'seeds: [\d ]+', data)
seeds = [int(x) for x in re.findall(r'(\d+)', m.group(0))]

maps = re.findall(r'\w+-to-\w+ map:((?:\s+\d+)+)', data)
for i in range(len(maps)):
    maps[i] = [[int(y) for y in x] for x in re.findall(r'(\d+) (\d+) (\d+)', maps[i])]


def map_one_seed(seed):
    for map in maps:
        dest = None
        for line in map:
            if line[1] <= seed <= line[1] + line[2] - 1:
                dest = line[0] + seed - line[1]
        if dest is None:
            dest = seed
        seed = dest

    return seed


print(min([map_one_seed(seed) for seed in seeds]))
