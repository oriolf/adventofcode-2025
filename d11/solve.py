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

example2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""


def parse_input(input):
    devices = {"out": []}
    for line in input:
        device, connections = line.split(":")
        connections = [x.strip() for x in connections.strip().split(" ")]
        devices[device] = connections

    return devices


def count_paths(devices, origin, destiny):
    if origin == destiny:
        return 1
    return sum(count_paths(devices, conn, destiny) for conn in devices[origin])


CACHE = {}


def count_paths_dac_fft(devices, origin, destiny):
    if origin == destiny:
        return 1

    global CACHE
    key = (origin, destiny)
    if key in CACHE:
        return CACHE[key]

    res = sum(count_paths_dac_fft(devices, conn, destiny) for conn in devices[origin])
    CACHE[key] = res
    return res


def solve1(input):
    devices = parse_input(input)
    return count_paths(devices, "you", "out")


def solve2(input):
    devices = parse_input(input)

    global CACHE
    CACHE = {}

    svr_fft = count_paths_dac_fft(devices, "svr", "fft")
    fft_dac = count_paths_dac_fft(devices, "fft", "dac")
    dac_out = count_paths_dac_fft(devices, "dac", "out")

    svr_dac = count_paths_dac_fft(devices, "svr", "dac")
    dac_fft = count_paths_dac_fft(devices, "dac", "fft")
    fft_out = count_paths_dac_fft(devices, "fft", "out")

    return svr_fft * fft_dac * dac_out + svr_dac * dac_fft * fft_out


assert solve1(example.split("\n")) == 5
assert solve2(example2.split("\n")) == 2
