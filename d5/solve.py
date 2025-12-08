example = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""


def parse_input(input):
    in_ranges = True
    ranges, ids = [], []
    for line in input:
        line = line.strip()
        if line == "":
            in_ranges = False
        elif in_ranges:
            x, y = line.split("-")
            ranges.append((int(x), int(y)))
        else:
            ids.append(int(line))

    return merge_ranges(ranges), ids


def ranges_overlap(a, b):
    lowa, higha = a
    lowb, highb = b
    if lowa < lowb:
        return higha >= lowb

    return highb >= lowa


def merge_range(a, b):
    lowa, higha = a
    lowb, highb = b
    return (min(lowa, lowb), max(higha, highb))


def add_range(new_ranges, new_range):
    for j, old_range in enumerate(new_ranges):
        if ranges_overlap(new_range, old_range):
            new_ranges[j] = merge_range(new_range, old_range)
            return new_ranges
    new_ranges.append(new_range)
    return new_ranges


def merge_ranges(ranges):
    n = len(ranges)
    new_ranges = merge_ranges_aux(ranges)
    while len(new_ranges) < n:
        n = len(new_ranges)
        new_ranges = merge_ranges_aux(new_ranges)

    return new_ranges


def merge_ranges_aux(ranges):
    new_ranges = []
    for i, new_range in enumerate(ranges):
        new_ranges = add_range(new_ranges, new_range)

    return new_ranges


def is_fresh(id, ranges):
    for low, high in ranges:
        if id >= low and id <= high:
            return True
    return False


def solve1(input):
    ranges, ids = parse_input(input)
    return sum(is_fresh(id, ranges) for id in ids)


def solve2(input):
    ranges, _ = parse_input(input)
    total = 0
    for low, high in ranges:
        total += high - low + 1
    return total


assert solve1(example.split("\n")) == 3
assert solve2(example.split("\n")) == 14
