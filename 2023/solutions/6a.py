# pushed_time: x
# (tot_time - x) * x > tot_distance
# tot_time * x - x^2 - tot_distance > 0
# x^2 - tot_time * x + tot_distance < 0
# x = (tot_time +- sqrt(tot_time^2 - 4 * tot_distance)) / 2

import re
from math import sqrt, floor, ceil

# with open('data/6a') as fh:
with open('data/6b') as fh:
    data = fh.readlines()

times = list(map(int, re.findall(r'\d+', data[0])))
dists = list(map(int, re.findall(r'\d+', data[1])))

tot = 1
for i in range(0, len(times)):
    low = floor((times[i] - sqrt(times[i]**2 - 4 * dists[i])) / 2 + 1)
    high = ceil((times[i] + sqrt(times[i]**2 - 4 * dists[i])) / 2 - 1)
    tot *= (high - low + 1)

print(tot)
