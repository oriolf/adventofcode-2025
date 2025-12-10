import math

from collections import defaultdict

example = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""


class Connections:
    def __init__(self):
        self.connection_count = 0
        self.points = {}
        self.groups = defaultdict(set)
        self.group_id = 0

    def get_group_id(self):
        self.group_id += 1
        return self.group_id

    def add_connection(self, a, b):
        self.connection_count += 1

        if a not in self.points and b not in self.points:
            id = self.get_group_id()
            self.groups[id] = set([a, b])
            self.points[a] = id
            self.points[b] = id
        elif a not in self.points:
            id = self.points[b]
            self.groups[id].add(a)
            self.points[a] = id
        elif b not in self.points:
            id = self.points[a]
            self.groups[id].add(b)
            self.points[b] = id
        elif self.points[a] == self.points[b]:
            pass  # already joined
        else:
            id_a = self.points[a]
            id_b = self.points[b]
            group_b = self.groups[id_b]
            for x in group_b:
                self.groups[id_a].add(x)
                self.points[x] = id_a
            del self.groups[id_b]

    def top_three(self):
        counts = [len(self.groups[id]) for id in self.groups]
        counts = sorted(counts, reverse=True)
        return counts[:3]

    def have_one_group(self, count):
        return len(self.points) == count and len(self.groups) == 1


def parse_input(input):
    points = []
    for row in input:
        x, y, z = row.split(",")
        points.append((int(x), int(y), int(z)))

    return points


def compute_pairs_distances(points):
    distances = []
    for i, a in enumerate(points):
        for b in points[i + 1 :]:
            distances.append((a, b, distance(a, b)))
    return distances


def distance(a, b):
    diff = (a[0] - b[0], a[1] - b[1], a[2] - b[2])
    return math.hypot(*diff)


def solve1(input):
    points = parse_input(input)
    distances = compute_pairs_distances(points)
    distances = sorted(distances, key=lambda x: x[2])
    connections = Connections()

    max_connections = 1000
    if len(points) < 1000:
        max_connections = 10

    i = 0
    while connections.connection_count < max_connections:
        a, b, _ = distances[i]
        connections.add_connection(a, b)
        i += 1

    a, b, c = connections.top_three()

    return a * b * c


def solve2(input):
    points = parse_input(input)
    distances = compute_pairs_distances(points)
    distances = sorted(distances, key=lambda x: x[2])
    connections = Connections()

    max_connections = 1000
    if len(points) < 1000:
        max_connections = 20

    i = 0
    while not connections.have_one_group(max_connections):
        a, b, _ = distances[i]
        connections.add_connection(a, b)
        i += 1

    return a[0] * b[0]


assert solve1(example.split("\n")) == 40
assert solve2(example.split("\n")) == 25272
