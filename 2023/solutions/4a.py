import re
import pandas as pd

points = 0
data = []
# with open('/tmp/example') as fh:
with open('4.txt') as fh:
    for line in fh.readlines():
        m = re.search(r'Card +(\d+): +([\d ]+) \| +([\d ]+)', line)
        if not m:
            raise ValueError(line)
        card, winning, have = m.groups()

        won = set(re.findall(r'(\d+)', winning)).intersection(re.findall(r'(\d+)', have))
        points += 2**(len(won)-1) if won else 0
        data.append({"card": int(card), "matches": len(won)})
        # print(won)

tab = pd.DataFrame(data)
tab = tab.set_index("card")
tab['count'] = 1

stack = list(tab.index)

# count = 0
while stack:
    # count += 1
    i = stack.pop(0)
    more = list(range(i+1, i+1+tab.matches.loc[i]))
    # stack = more + stack
    for j in more:
        tab['count'].loc[j] += tab['count'].loc[i]


print(tab['count'].sum())


# Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
# Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
# Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
# Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
# Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
# Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
