def main(file):
    with open(file) as fh:
        a = fh.readline().rstrip().split(',')

    print(sum(process(x) for x in a))


def process(x: str):
    cur = 0
    for c in x:
        cur = (cur + ord(c)) * 17 % 256
    return cur


process('cm-')

main('data/15')
# main('/tmp/example')
