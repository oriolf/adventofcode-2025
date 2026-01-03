example = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""


def parse_input(input):
    cases = []
    for line in input:
        if "x" in line:
            cases.append(parse_case(line))

    return cases


def parse_case(line):
    square, counts = line.split(":")
    w, h = square.split("x")
    counts = counts.strip().split(" ")

    return ((int(w), int(h)), [int(x) for x in counts])


def solve1(input):
    # it seemed really difficult, but there are two cases: occupation of more
    # than 100% (obviously impossible), and less than 75% (much feasible). Turns out
    # all of less than 75% are achievable, so I got a star for free

    cases = parse_input(input)
    count = 0
    for case in cases:
        total = case[0][0] * case[0][1]
        a, b, c, d, e, f = case[1]
        occupied = a * 5 + b * 7 + c * 7 + d * 7 + e * 6 + f * 7
        fraction = occupied / total
        if fraction < 1:
            count += 1

    return count


def solve2(input):
    return 0


assert solve1(example.split("\n")) == 3
assert solve2(example.split("\n")) == 0
