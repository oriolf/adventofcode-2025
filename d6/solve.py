example = (
    "123 328  51 64 \n" + " 45 64  387 23 \n" + "  6 98  215 314\n" + "*   +   *   +  "
)


def parse_input(input):
    new_input = []
    for i, row in enumerate(input):
        if i == len(input) - 1:
            new_input.append([x.strip() for x in row.split(" ") if x != ""])
        else:
            new_input.append([int(x.strip()) for x in row.split(" ") if x != ""])

    return list(zip(*new_input))


def all_blank(row):
    return "".join(row).strip() == ""


def has_operator(row):
    return row[-1] != " "


def extract_number(row):
    return int("".join(row))


def parse_input2(input):
    new_input = list(zip(*[list(x) for x in input]))
    operations = []
    operator, op = "", []
    for row in new_input:
        if all_blank(row):
            op.append(operator)
            operations.append(op)
            op = []
        elif has_operator(row):
            op.append(extract_number(row[:-1]))
            operator = row[-1]
        else:
            op.append(extract_number(row))

    op.append(operator)
    operations.append(op)
    return operations


def compute_sum(lst):
    total = 0
    for x in lst:
        total += x
    return total


def compute_prod(lst):
    total = 1
    for x in lst:
        total *= x
    return total


def compute_operations(operations):
    total = 0
    for op in operations:
        if len(op) == 1:
            continue
        if op[-1] == "+":
            total += compute_sum(op[:-1])
        else:
            total += compute_prod(op[:-1])

    return total


def solve1(input):
    return compute_operations(parse_input(input))


def solve2(input):
    return compute_operations(parse_input2(input))


assert solve1(example.split("\n")) == 4277556
assert solve2(example.split("\n")) == 3263827
