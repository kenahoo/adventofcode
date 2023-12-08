import re


def main(file):
    trans = {}
    with open(file) as fh:
        lrs = fh.readline().strip()
        for line in fh.readlines():
            if re.match(r'^$', line):
                continue
            m = re.match(r'(\w+) = \((\w+), (\w+)\)', line)
            trans[m.group(1)] = {'L': m.group(2), 'R': m.group(3)}

    i = j = 0
    cur = 'AAA'
    while True:
        cur = trans[cur][lrs[j]]
        if cur == 'ZZZ':
            print(i+1)
            break
        i += 1
        j = (j + 1) % len(lrs)


main('data/8')
# main('/tmp/example2')
