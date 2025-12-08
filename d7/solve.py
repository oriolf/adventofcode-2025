from collections import defaultdict

example = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""


def solve1(input):
    positions = set([input[0].index("S")])
    count = 0
    for row in input[1:]:
        new_positions = set()
        for pos in positions:
            if row[pos] == "^":
                new_positions.add(pos - 1)
                new_positions.add(pos + 1)
                count += 1
            else:
                new_positions.add(pos)

        positions = new_positions

    return count


# took too long (but for the example it worked)
# def solve2(input):
#    return recursive_solve(input[0].index("S"), input[1:], 1)
#
#
# def recursive_solve(position, input, count):
#    for i, row in enumerate(input):
#        if row[position] == "^":
#            left = recursive_solve(position - 1, input[i:], count)
#            right = recursive_solve(position + 1, input[i:], count)
#            return left + right
#    return count


def solve2(input):
    positions = {input[0].index("S"): 1}
    for row in input[1:]:
        new_positions = defaultdict(int)
        for pos in positions.keys():
            if row[pos] == "^":
                new_positions[pos - 1] += positions[pos]
                new_positions[pos + 1] += positions[pos]
            else:
                new_positions[pos] += positions[pos]

        positions = new_positions

    return sum(positions.values())


assert solve1(example.split("\n")) == 21
assert solve2(example.split("\n")) == 40
