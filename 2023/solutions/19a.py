import re


def cond_to_code(cond):
    if re.match(r'^[AR]$', cond):
        return f"  return {cond == 'A'}"

    if m := re.match(r'([smax])([<>])(\d+):(\w+)', cond):
        result = m.group(4) == "A" if m.group(4) in "AR" else f"{m.group(4)}_(x)"
        return f'  if x["{m.group(1)}"]{m.group(2)}{m.group(3)}:\n    return {result}'

    if m := re.match(r'^([a-z]+)$', cond):
        return f"  return {m.group(1)}_(x)"

    raise RuntimeError(f"Unrecognized rule: {cond}")


def main(file):

    with open(file) as fh:
        rule_text, starts = fh.read().split('\n\n')

    for name, meat in re.findall(r'(\w+)\{([^}]+)}', rule_text):
        code = "\n".join([cond_to_code(cond) for cond in meat.split(',')])
        exec(f"def {name}_(x):\n{code}", globals())

    total = 0
    for meat in re.findall(r'\{([^}]+)\}', starts):
        point = eval(f"dict({meat})")
        if in_(point):
            total += sum(point.values())

    print(total)


main('data/19')
# main('/tmp/example')
