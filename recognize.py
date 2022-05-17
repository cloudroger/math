def add(a, b):
    return a + b


def mult(a, b):
    if b >= 0:
        return a * b
    elif b < 0:
        return a * (1 / abs(b))


def expo(a, b):
    if b >= 0:
        return a ** b
    elif b < 0:
        return a ** (1 / abs(b))


def intersect(errors):
    return min(errors) < 0


hyperops = [add, mult, expo]


def recognize(group, start=0):
    for index, hyperop in enumerate(hyperops):
        index += 1
        errors = []
        for i in range(3, len(group)):
            num = group[i]
            value = hyperop(i, i)
            errors.append(num - value)
        if intersect(errors):
            b_check = -1
            while True:
                b_check += 1
                for i in range(3, len(group)):
                    if hyperop(i, b_check) != group[i]:
                        success = False
                        break
                    success = True
                if success:
                    return hyperop, b_check
                    break
        else:
            continue


notation = {add:'*$n + {}$*',
            mult:'*$n * {}$*',
            expo:'*$n^{}$*'}


def get_markdown(hyperop, b_check):
    markdown = notation[hyperop].format(b_check)
    return markdown

def execute():
    print('Enter numbers:')
    x = input()
    group = [int(i) for i in x.split(',')]
    hyperop, b = recognize(group)
    return hyperop, b
