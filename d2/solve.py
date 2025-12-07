from utils import input


def id_ranges():
    row = input()[0]
    ranges = []
    for rang in row.split(","):
        x, y = rang.split("-")
        ranges.append((int(x), int(y)))
    return ranges


def valid_id(x, parts):
    s = str(x)
    if len(s) % parts != 0:
        return True

    delta = int(len(s) / parts)

    start, end = 0, delta
    while end < len(s):
        if s[start:end] != s[end : end + delta]:
            return True
        start += delta
        end += delta

    return False


def valid_id_2(x):
    for i in range(2, len(str(x)) + 1):
        if not valid_id(x, i):
            return False
    return True


def solve1():
    total = 0
    for low, high in id_ranges():
        for i in range(low, high + 1):
            if not valid_id(i, 2):
                total += i

    print(total)


def solve2():
    total = 0
    for low, high in id_ranges():
        for i in range(low, high + 1):
            if not valid_id_2(i):
                total += i

    print(total)
