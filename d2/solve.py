example = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""


def id_ranges(input):
    row = input[0]
    ranges = []
    for rang in row.split(","):
        x, y = rang.split("-")
        ranges.append((int(x), int(y)))
    return ranges


def valid_id(s, delta, length):
    start, end = 0, delta
    while end < length:
        if s[start:end] != s[end : end + delta]:
            return True
        start += delta
        end += delta

    return False


def remove_divisors(divisors):
    if len(divisors) > 1 and divisors[0] == 1:
        divisors.pop(0)
    if len(divisors) == 2 and divisors[0] == 2 and divisors[1] == 4:
        divisors.pop(0)
    return divisors


divisors = [[]]
divs = []
for i in range(1, 11):
    for j in range(1, 11):
        if i % j == 0:
            divs.append(j)
    divisors.append(remove_divisors(divs[:-1]))
    divs = []


def valid_id_2(s):
    length = len(s)
    for i in divisors[length]:
        if not valid_id(s, i, length):
            return False
    return True


def solve1(input):
    total = 0
    for low, high in id_ranges(input):
        for i in range(low, high + 1):
            s = str(i)
            length = len(s)
            if length % 2 == 0 and not valid_id(s, int(length / 2), length):
                total += i

    return total


def solve2(input):
    total = 0
    for low, high in id_ranges(input):
        for i in range(low, high + 1):
            if not valid_id_2(str(i)):
                total += i

    return total


assert solve1([example]) == 1227775554
assert solve2([example]) == 4174379265
