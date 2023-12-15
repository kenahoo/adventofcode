import re
from functools import cache


def parse_line(line, mult=1):
    text, lengths = line.rstrip().split(' ')
    return '?'.join([text] * mult), tuple(int(x) for x in lengths.split(',')) * mult


@cache
def matches(text, lengths: tuple):
    first_len, *more_lens = lengths
    more_lens = tuple(more_lens)  # Keep it hashable for caching

    pat = re.compile(f'[?#]{{{first_len}}}' + ('[^#]' if more_lens else '[^#]*$'))

    # Iterate through possible starting points
    count = 0
    for i in range(len(text)):
        if text[i] == '.':
            continue
        if re.match(pat, text[i:]):
            count += matches(text[i + first_len + 1:], more_lens) if more_lens else 1
        if text[i] == '#':
            # Must start a match here
            return count

    return count


def main(file, mult=1):
    with open(file) as fh:
        a = [parse_line(x, mult) for x in fh.readlines()]

    total = 0
    for text, counts in a:
        print(f"Starting pattern: {text}   --   {','.join([str(x) for x in counts])}")
        total += matches(text, counts)
        print(f"Matches: {matches(text, counts)}")
    print(total)


main('data/12', 5)
# main('/tmp/example', 5)
