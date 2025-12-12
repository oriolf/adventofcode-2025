example = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""


def parse_input(input):
    devices = {}
    for line in input:
        device, connections = line.split(":")
        connections = [x.strip() for x in connections.strip().split(" ")]
        devices[device] = connections

    return devices


def count_paths(devices, origin, destiny):
    if origin == destiny:
        return 1
    return sum(count_paths(devices, conn, destiny) for conn in devices[origin])


def solve1(input):
    devices = parse_input(input)
    return count_paths(devices, "you", "out")


def solve2(input):
    return 0


assert solve1(example.split("\n")) == 5
assert solve2(example.split("\n")) == 0
