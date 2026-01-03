import numpy

from scipy.optimize import linprog

example = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""


class Machine:
    def __init__(self, line):
        parts = line.strip().split(" ")
        self.buttons = []
        for part in parts:
            if part.startswith("["):
                self.lights = part[1:-1]
            elif part.startswith("("):
                self.buttons.append([int(x) for x in part[1:-1].split(",")])
            else:
                self.joltages = [int(x) for x in part[1:-1].split(",")]


class Column:
    def __init__(self, values, index):
        self.values = values
        self.index = index

    def __str__(self):
        return str(self.values)


class LinearEquations:
    def __init__(self, columns, independent_terms):
        self.columns = [Column(col, i) for i, col in enumerate(columns)]
        self.independent_terms = independent_terms
        self.counts = [0] * len(columns)
        self.solved = [False] * len(columns)

    def duplicate_without_col(self, i):
        le = LinearEquations([], self.independent_terms)
        le.columns = [
            Column(list(c.values), c.index)
            for j, c in enumerate(self.columns)
            if i != j
        ]
        le.counts = list(self.counts)
        le.solved = list(self.solved)

        return le

    def solve(self):
        # if matrix has more rows than columns or determinant == 0, discard rows that are linearly dependent on the others
        # repeat the process until the matrix is squared with determinant != 0 and solve linear equation
        while not all(self.solved):
            if len(self.columns) > len(self.columns[0].values):
                sols = []
                for new_sols in [le.solve() for le in self.remove_column()]:
                    for sol in new_sols:
                        sols.append(sol)
                return sols
            elif len(self.columns[0].values) > len(self.columns) or self.det() == 0:
                self.remove_row()
            else:
                results = self.solve_linear()
                for i, res in enumerate(results):
                    col_index = self.columns[i].index
                    self.counts[col_index] = res
                    self.solved[col_index] = True
                return [self.counts]

    # if matrix has more columns than rows, select columns with most 1s,
    # substract to joltages, record quantity of button presses (how many times
    # the column was subtracted), remove column, until matrix square
    def remove_column(self):
        for i in self.column_indexes_with_max_sum():
            col = self.columns[i]
            le = self.duplicate_without_col(i)
            # compute n how much times we can do independent_terms - col
            n = self.count_how_many_times_contained(le.independent_terms, col.values)
            to_subtract = le.multiply(n, col.values)
            le.independent_terms = le.subtract(le.independent_terms, to_subtract)
            le.counts[col.index] = n
            le.solved[col.index] = True
            yield le

    def remove_row(self):
        matrix = self.matrix_in_rows()
        rank = self.rank()
        for i in range(len(matrix)):
            new_matrix = list(matrix)
            new_matrix.pop(i)
            if rank == numpy.linalg.matrix_rank(new_matrix):
                self.remove_nth_row(i)
                return

    def remove_nth_row(self, index):
        for i in range(len(self.columns)):
            self.columns[i].values.pop(index)
        self.independent_terms.pop(index)

    def column_indexes_with_max_sum(self):
        lst = [(i, sum(col.values)) for i, col in enumerate(self.columns)]
        lst = sorted(lst, key=lambda x: x[1], reverse=True)
        return [x[0] for x in lst if x[1] == lst[0][1]]

    def det(self):
        return numpy.linalg.det(self.matrix_in_rows())

    def rank(self):
        return numpy.linalg.matrix_rank(self.matrix_in_rows())

    def rank_removing_col(self, i):
        columns = list(self.columns)
        columns.pop(i)
        return LinearEquations([col.values for col in columns], []).rank()

    def solve_linear(self):
        return numpy.linalg.solve(self.matrix_in_rows(), self.independent_terms)

    def matrix_in_rows(self):
        return list(zip(*[list(col.values) for col in self.columns]))

    def multiply(self, n, lst):
        return [n * x for x in lst]

    def subtract(self, a, b):
        if len(a) != len(b):
            raise Exception("Wrong sizes!")
        return [a[i] - b[i] for i in range(len(a))]

    def count_how_many_times_contained(self, a, b):
        n = 1
        subtracted = self.subtract(a, self.multiply(n, b))
        while all([x >= 0 for x in subtracted]):
            n += 1
            subtracted = self.subtract(a, self.multiply(n, b))
        return n - 1


def parse_input(input):
    return [Machine(line) for line in input]


def transpose(cols):
    return list(zip(*[list(col) for col in cols]))


def press_button(light, button):
    lst = list(light)
    for i in button:
        if lst[i] == "#":
            lst[i] = "."
        else:
            lst[i] = "#"

    return "".join(lst)


def minimum_button_presses(machine):
    lights = set(["." * len(machine.lights)])
    i = 0
    while machine.lights not in lights:
        i += 1
        lights = set(
            press_button(light, button)
            for light in lights
            for button in machine.buttons
        )

    return i


def button_column(button, n):
    col = [0] * n
    for i in button:
        col[i] = 1
    return col


def minimum_button_presses_for_joltages(machine):
    columns = [
        button_column(button, len(machine.joltages)) for button in machine.buttons
    ]
    equations = LinearEquations(columns, machine.joltages)
    res = equations.solve()
    res = [r for r in res if all(x >= 0 for x in r)]
    res = [sum(r) for r in res]
    return min(res)


def bases(matrix, length, base):
    if length == 0 and numpy.linalg.matrix_rank(base) == len(base):
        yield base

    if length > 0:
        for i, col in enumerate(matrix):
            yield from bases(matrix[i + 1 :], length - 1, base + [col])


def remove_linearly_dependent_row(rank, matrix, b):
    for i in range(len(matrix)):
        new_matrix = matrix[:i] + matrix[i + 1 :]
        if numpy.linalg.matrix_rank(new_matrix) == rank:
            matrix = new_matrix
            return new_matrix, b[:i] + b[i + 1 :]


def remove_linearly_dependent_rows(matrix, b):
    rank = numpy.linalg.matrix_rank(matrix)
    while len(matrix) > rank:
        matrix, b = remove_linearly_dependent_row(rank, matrix, b)

    return matrix, b


def almost_int(x):
    return abs(x - float(int(x))) < 1e-5


def solve_bases(machine):
    A = [button_column(button, len(machine.joltages)) for button in machine.buttons]
    b = machine.joltages
    minimum = 123456789
    for base in bases(A, numpy.linalg.matrix_rank(A), []):
        Ai, bi = remove_linearly_dependent_rows(transpose(base), b)
        sol = numpy.linalg.solve(Ai, bi)
        if all(x >= -1e-14 and almost_int(x) for x in sol):
            if sum(sol) < minimum:
                minimum = sum(sol)

    return int(minimum)
    # Returns 18770, correct answer is 18771, so in all cases but one, a fractional
    # solution can be resolved using just one extra button
    # if minimum == round(minimum):
    #    return int(minimum)
    # return int(round(minimum)) + 1


def simplex(machine):
    columns = [
        button_column(button, len(machine.joltages)) for button in machine.buttons
    ]
    A = transpose(columns)
    res = linprog(
        [1] * len(machine.buttons), A_eq=A, b_eq=machine.joltages, integrality=1
    )
    return int(res.fun)


def solve1(input):
    machines = parse_input(input)
    return sum(minimum_button_presses(machine) for machine in machines)


def solve2(input):
    machines = parse_input(input)
    # does not work and I don't know if it's fixable
    # return sum(minimum_button_presses_for_joltages(machine) for machine in machines)
    return sum(solve_bases(machine) for machine in machines)


# le = LinearEquations([[1, 2], [3, 4]], [4, 6])
# assert le.rank() == 2
# assert le.matrix_in_rows()[0][1] == 3
# assert le.matrix_in_rows()[1][0] == 2
# assert le.solve_linear()[0] == 1
# assert le.solve_linear()[1] == 1
# le.remove_nth_row(0)
# assert len(le.columns[0].values) == 1
# assert le.columns[0].values[0] == 2

assert solve1(example.split("\n")) == 7
assert solve2(example.split("\n")) == 33
