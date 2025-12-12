from collections import defaultdict

example = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""


def parse_input(input):
    points = []
    for line in input:
        x, y = line.split(",")
        points.append((int(x), int(y)))
    return points


def compute_area(p1, p2):
    width = abs(p1[0] - p2[0]) + 1
    height = abs(p1[1] - p2[1]) + 1
    return width * height


def solve1(input):
    points = parse_input(input)
    maximum = 0
    for i, p1 in enumerate(points):
        for p2 in points[i + 1 :]:
            area = compute_area(p1, p2)
            if area > maximum:
                maximum = area

    return maximum


def solve2(input):
    return 0


assert solve1(example.split("\n")) == 50
assert solve2(example.split("\n")) == 0
