import re
from collections import Counter

cards = 'J23456789TQKA'
ranks = {c: i for i, c in enumerate(cards)}


def rank(hand: str) -> list[int]:
    return [ranks[x] for x in hand]


def hand_type(hand: str) -> int:
    if hand == 'JJJJJ':
        return hand_type('AAAAA')

    counts = Counter(hand)
    j_count = counts.pop('J', 0)
    counts[counts.most_common(1)[0][0]] += j_count

    mc = counts.most_common()
    if len(counts) == 1:  # Five of a kind
        return 5
    if len(counts) == 2:
        if mc[0][1] == 4:  # Four of a kind
            return 4
        if mc[0][1] == 3:  # Full house
            return 3
    if len(counts) == 3:
        if mc[0][1] == 3:  # Three of a kind
            return 2
        if mc[0][1] == 2:  # Two pair
            return 1
    if len(counts) == 4:  # One pair
        return 0
    if len(counts) == 5:  # High card
        return -1
    raise ValueError(f"Bad hand: {hand}")


def main(file):
    hands = []
    with open(file) as fh:
        for line in fh.readlines():
            m = re.match(r'(\w+) (\d+)', line)
            if not m:
                raise ValueError(f"Bad line: {line}")
            hand, bid = m.groups()
            hands.append([hand_type(hand), rank(hand), int(bid)])

    hands = sorted(hands, key=lambda x: [x[0], x[1]])

    tot = 0
    for i, hand in enumerate(hands):
        tot += hand[2] * (i+1)

    print(tot)


main('data/7')
