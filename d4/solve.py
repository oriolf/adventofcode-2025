example = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

DIRECTIONS = [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if x != 0 or y != 0]


def count_adjacent(input, i, j):
    count = 0
    for x, y in DIRECTIONS:
        if i + x >= 0 and i + x < len(input) and j + y >= 0 and j + y < len(input[i]):
            if input[i + x][j + y] == "@":
                count += 1

    return count


def remove_rolls(input):
    new_input = [list(row) for row in input]
    for i, row in enumerate(input):
        for j, col in enumerate(row):
            if col == "@" and count_adjacent(input, i, j) < 4:
                new_input[i][j] = "."

    return new_input


def solve1(input):
    count = 0
    for i, row in enumerate(input):
        for j, col in enumerate(row):
            if col == "@" and count_adjacent(input, i, j) < 4:
                count += 1

    return count


def solve2(input):
    input = [list(x) for x in input]
    total = 0
    while True:
        count = solve1(input)
        if count == 0:
            break
        input = remove_rolls(input)
        total += count

    return total


assert solve1(example.split("\n")) == 13
assert solve2(example.split("\n")) == 43
