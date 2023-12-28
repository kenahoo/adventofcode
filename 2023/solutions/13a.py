def num_dif(a, b):
    return sum(1 for x, y in zip(a, b) if x != y)


def process_chunk(rows, smudges=0):
    for i in range(1, len(rows)):
        num_different = 0
        # Check if the mirror is here
        num_out = min(i, len(rows)-i)
        for j in range(1, num_out+1):
            # print(f"Checking mirror row {i}: {i-j} and {i+j-1}")
            num_different += num_dif(rows[i-j], rows[i+j-1])
            if num_different > smudges:
                break
        else:
            # All rows were ok
            if num_different == smudges:
                return i

    return None


def transpose(rows):
    return list(''.join(x) for x in zip(*rows))


def main(file, smudges=0):

    total = 0
    with open(file) as fh:
        for chunk in fh.read().split('\n\n'):
            rows = chunk.rstrip().split('\n')
            result = process_chunk(rows, smudges)
            if result:
                # print(f"Found at row {result}")
                total += 100 * result
            else:
                result = process_chunk(transpose(rows), smudges)
                # print(f"Found at column {result}")
                if result:
                    total += result
                else:
                    raise Exception("No result found")

    print(total)


# Part A:
main('data/13')
# main('/tmp/example')

# Part B:
main('data/13', 1)
