from utils import input


def convert(x):
    if x.startswith("R"):
        return int(x[1:])
    return -int(x[1:])


def solve1():
    position, count = 50, 0
    for movement in [convert(x) for x in input()]:
        position += movement
        position %= 100
        if position == 0:
            count += 1

    print(count)


def solve2():
    position, count = 50, 0
    for movement in [convert(x) for x in input()]:
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

    print(count)
