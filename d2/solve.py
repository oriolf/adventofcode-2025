example = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""


def id_ranges(input):
    row = input[0]
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


def solve1(input):
    total = 0
    for low, high in id_ranges(input):
        for i in range(low, high + 1):
            if not valid_id(i, 2):
                total += i

    return total


def solve2(input):
    total = 0
    for low, high in id_ranges(input):
        for i in range(low, high + 1):
            if not valid_id_2(i):
                total += i

    return total


assert solve1([example]) == 1227775554
assert solve2([example]) == 4174379265
