from PIL import Image
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
    global BOUNDING_BOX
    points = []
    minx, maxx, miny, maxy = 1e10, -1, 1e10, -1
    for line in input:
        x, y = line.split(",")
        p = (int(x), int(y))
        if p[0] < minx:
            minx = p[0]
        if p[0] > maxx:
            maxx = p[0]
        if p[1] < miny:
            miny = p[1]
        if p[1] > maxy:
            maxy = p[1]
        points.append(p)

    BOUNDING_BOX = (minx, maxx, miny, maxy)
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


def sides(p1, p2):
    return [
        (p1, (p1[0], p2[1])),
        (p1, (p2[0], p1[1])),
        (p2, (p2[0], p1[1])),
        (p2, (p1[0], p2[1])),
    ]


def valid_pair(p1, p2, edges, corners):
    for e in sides(p1, p2):
        if not valid_edge(e, edges, corners):
            return False
    return True


def valid_edge(e, edges, corners):
    for p in points_check_edge(e[0], e[1], edges):
        if not point_inside(p, edges, corners):
            return False
    return True


INSIDE_CACHE = {}
BOUNDING_BOX = None


def closest_outside(p):
    global BOUNDING_BOX
    minx, maxx, miny, maxy = BOUNDING_BOX

    points = sorted(
        [
            ((p[0], miny - 1), abs(p[1] - miny)),
            ((p[0], maxy + 1), abs(p[1] - maxy)),
            ((minx - 1, p[1]), abs(p[0] - minx)),
            ((maxx + 1, p[1]), abs(p[0] - maxx)),
        ],
        key=lambda x: x[1],
    )
    return points[0][0]


def point_inside(p, edges, corners):
    global INSIDE_CACHE
    if p in INSIDE_CACHE:
        return INSIDE_CACHE[p]

    if p in edges:
        INSIDE_CACHE[p] = True
        return True

    edges_crossed = set()
    corner_edges_crossed = set()
    for p in points_between(p, closest_outside(p)):
        if p in edges:
            for edge in edges[p]:
                edges_crossed.add(edge)
        if p in corners:
            for edge in corners[p]:
                corner_edges_crossed.add(edge)

    res = len(edges_crossed - corner_edges_crossed) % 2 == 1
    INSIDE_CACHE[p] = res
    return res


def compute_edge(points):
    edges, corners = defaultdict(set), defaultdict(set)
    for i in range(len(points) - 1):
        add_edge(edges, points[i], points[i + 1], i)
        corners[points[i]].add(i)
        corners[points[i + 1]].add(i)
    add_edge(edges, points[-1], points[0], i + 1)
    corners[points[-1]].add(i + 1)
    corners[points[0]].add(i + 1)
    return edges, corners


def add_edge(edges, p1, p2, i):
    for p in points_between(p1, p2):
        edges[p].add(i)


def points_between(p1, p2):
    if p1[0] == p2[0]:
        low, high = min(p1[1], p2[1]), max(p1[1], p2[1])
        for i in range(low, high + 1):
            yield (p1[0], i)

    if p1[1] == p2[1]:
        low, high = min(p1[0], p2[0]), max(p1[0], p2[0])
        for i in range(low, high + 1):
            yield (i, p1[1])


def points_check_edge(p1, p2, edges):
    on_edge = True
    points = list(points_between(p1, p2))
    for p in points:
        if p not in edges and on_edge:
            yield p
            on_edge = False
        elif p in edges and not on_edge:
            on_edge = True
    on_edge = True
    for p in points[::-1]:
        if p not in edges and on_edge:
            yield p
            on_edge = False
        elif p in edges and not on_edge:
            on_edge = True


# for debugging purposes; doesn't work, 50MB SVG does not load at all
def write_svg(p1, p2, points):
    with open("map.svg", "w") as f:
        f.write("<svg>")
        for i in range(len(points) - 1):
            f.write(
                f'<line x1="{p1[0]}" y1="{p1[1]}" x2="{p2[0]}" y2="{p2[1]}" style="stroke:black;stroke-width:1" />'
            )
        f.write("</svg>")


def write_svg_side(p1, p2, points):
    i1, i2 = points.index(p1), points.index(p2)
    with open("map.svg", "w") as f:
        f.write("<svg>")
        for s in sides(p1, p2):
            f.write(
                f'<line x1="{s[0][0]}" y1="{s[0][1]}" x2="{s[1][0]}" y2="{s[1][1]}" style="stroke:red;stroke-width:1" />'
            )
        for i in range(i1, i2 + 1):
            p1, p2 = points[i], points[i + 1]
            f.write(
                f'<line x1="{p1[0]}" y1="{p1[1]}" x2="{p2[0]}" y2="{p2[1]}" style="stroke:black;stroke-width:1" />'
            )

        f.write("</svg>")


# for debugging purposes; doesn't work, process gets killed, raw image would occupy 40GB
def write_bitmap(p1, p2, points):
    width, height = 0, 0
    for p in points:
        if p[0] > width:
            width = p[0] + 1
        if p[1] > height:
            height = p[1] + 1

    img = Image.new("RGB", (width, height), "white")
    pixels = img.load()
    for i in range(len(points) - 1):
        for p in points_between(points[i], points[i + 1]):
            pixels[p[0], p[1]] = (0, 0, 0)

    img.save("map.bmp")


def compute_rectangles_areas(points):
    for i, p1 in enumerate(points):
        for p2 in points[i + 1 :]:
            area = compute_area(p1, p2)
            yield (p1, p2, area)


def solve2(input):
    global INSIDE_CACHE
    points = parse_input(input)
    edge, corners = compute_edge(points)
    INSIDE_CACHE = {}

    rectangles = sorted(
        compute_rectangles_areas(points),
        key=lambda x: x[2],
        reverse=True,
    )
    for rect in rectangles:
        valid = valid_pair(rect[0], rect[1], edge, corners)
        if valid:
            break

    return rect[2]


assert solve1(example.split("\n")) == 50
assert solve2(example.split("\n")) == 24
