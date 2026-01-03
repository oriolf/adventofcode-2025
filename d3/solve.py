example = """987654321111111
811111111111119
234234234234278
818181911112111"""


def update_maxes(i, x, n, digits, maxes):
    for j, m in enumerate(maxes):
        if m is None or (x > m and i < n - (digits - j - 1)):
            maxes[j] = x
            if j < len(maxes) - 1:
                maxes[j + 1] = None
            return maxes
    return maxes


def joltage(bank, digits):
    maxes = [None] * digits
    for i, s in enumerate(bank):
        maxes = update_maxes(i, int(s), len(bank), digits, maxes)

    total, multiplier = 0, 1
    for x in maxes[::-1]:
        total += x * multiplier
        multiplier *= 10

    return total


def solve1(input):
    return sum(joltage(bank.strip(), 2) for bank in input)


def solve2(input):
    return sum(joltage(bank.strip(), 12) for bank in input)


assert solve1(example.split("\n")) == 357
assert solve2(example.split("\n")) == 3121910778619
