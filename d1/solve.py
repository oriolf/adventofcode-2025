example = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""


def convert(x):
    if x.startswith("R"):
        return int(x[1:])
    return -int(x[1:])


def solve1(input):
    position, count = 50, 0
    for movement in [convert(x) for x in input]:
        position += movement
        position %= 100
        if position == 0:
            count += 1

    return count


def solve2(input):
    position, count = 50, 0
    for movement in [convert(x) for x in input]:
        if movement > 0:
            count += movement // 100
            movement %= 100
            if position != 0 and position + movement >= 100:
                count += 1
        elif movement < 0:
            count += -movement // 100
            movement = -(-movement % 100)
            if position != 0 and position + movement <= 0:
                count += 1

        position += movement
        position %= 100

    return count


assert solve1(example.split("\n")) == 3
assert solve2(example.split("\n")) == 6
