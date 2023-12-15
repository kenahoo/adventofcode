import re


def parse_line(line):
    text, lengths = line.rstrip().split(' ')
    lengths = lengths.split(',')
    return text, re.compile(r'\.*' + r'\.+'.join([f'#{{{l}}}' for l in lengths]) + r'\.*$')


def realizations(text):
    locations = [i for i, x in enumerate(text) if x == '?']
    text_array = list(text)
    for i in range(2 ** len(locations)):
        for j, loc in enumerate(locations):
            text_array[loc] = '.' if (i >> j) & 1 else '#'
        yield ''.join(text_array)


def main(file):
    with open(file) as fh:
        a = [parse_line(x) for x in fh.readlines()]

    total = 0
    for text, regex in a:
        print(f"Starting pattern: {text}")
        for r in realizations(text):
            if regex.match(r):
                print(f"Match: {r}")
                total += 1
        print()
    print(total)


main('data/12')
