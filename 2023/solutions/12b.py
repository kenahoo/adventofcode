import re
from functools import cache


def parse_line(line, mult=1):
    text, lengths = line.rstrip().split(' ')
    return '?'.join([text] * mult), tuple(int(x) for x in lengths.split(',')) * mult


@cache
def matches(text, lengths: tuple):  # Keep it hashable for caching
    first, *more = lengths
    pat = re.compile(f'[?#]{{{first}}}' + ('[^#]' if more else '[^#]*$'))

    # Iterate through possible starting points
    count = 0
    for i in range(len(text)):
        if text[i] == '.':
            continue
        if re.match(pat, text[i:]):
            count += matches(text[i + first + 1:], tuple(more)) if more else 1
        if text[i] == '#':
            # Must start a match here
            return count

    return count


def main(file, mult=1):
    with open(file) as fh:
        a = [parse_line(x, mult) for x in fh.readlines()]

    print(sum(matches(text, counts) for text, counts in a))


main('data/12', 5)
# main('/tmp/example', 5)
