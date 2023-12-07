import re
from collections import Counter

cards = '23456789TJQKA'
ranks = {c: i for i, c in enumerate(cards)}


def rank(hand: str) -> list[int]:
    return [ranks[x] for x in hand]


def hand_type(hand: str) -> tuple:
    counts = Counter(hand)
    mc = counts.most_common()
    if len(counts) == 1:  # Five of a kind
        return 5, rank(hand)
    if len(counts) == 2:
        if mc[0][1] == 4:  # Four of a kind
            return 4, rank(hand)
        if mc[0][1] == 3:  # Full house
            return 3, rank(hand)
    if len(counts) == 3:
        if mc[0][1] == 3:  # Three of a kind
            return 2, rank(hand)
        if mc[0][1] == 2:  # Two pair
            return 1, rank(hand)
    if len(counts) == 4:  # One pair
        return 0, rank(hand)
    if len(counts) == 5:  # High card
        return -1, rank(hand)
    raise ValueError(f"Bad hand: {hand}")


hands = []
# with open('/tmp/example') as fh:
with open('data/7') as fh:
    for line in fh.readlines():
        m = re.match(r'(\w+) (\d+)', line)
        if not m:
            raise ValueError(f"Bad line: {line}")
        hands.append([hand_type(m.group(1)), int(m.group(2))])


hands = sorted(hands, key=lambda x: x[0])

tot = 0
for i, hand in enumerate(hands):
    tot += hand[1] * (i+1)

print(tot)
# print(hands)
