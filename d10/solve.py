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
                self.unknown = [int(x) for x in part[1:-1].split(",")]


def parse_input(input):
    return [Machine(line) for line in input]


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


def solve1(input):
    machines = parse_input(input)
    return sum(minimum_button_presses(machine) for machine in machines)


def solve2(input):
    return 0


assert solve1(example.split("\n")) == 7
assert solve2(example.split("\n")) == 0
