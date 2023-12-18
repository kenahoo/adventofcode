import re


def box_action(label, operation, value, box):
    # Modifies box in-place
    for i, val in enumerate(box):
        if val[0].startswith(label):
            if operation == '-':
                box.pop(i)
            elif operation == '=':
                box[i] = [label, value]
            return

    if operation == '=':
        box.append([label, value])


def checksum(boxes):
    return sum([(i + 1) * (j + 1) * int(lens[1]) for i, box in enumerate(boxes) for j, lens in enumerate(box)])


def main(file):
    with open(file) as fh:
        a = fh.readline().rstrip().split(',')

    boxes = [[] for _ in range(256)]
    for step in a:
        label, operation, value = re.match(r'(.+)([-=])(\d*)', step).groups()
        box_action(label, operation, value, boxes[process(label)])

    print(checksum(boxes))


def process(x: str):
    cur = 0
    for c in x:
        cur = (cur + ord(c)) * 17 % 256
    return cur


main('data/15')
