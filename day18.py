from collections import namedtuple


Point = namedtuple("Point", "x y")
facings = [
    Point(0, 1),  # Up
    Point(1, 0),  # Right
    Point(0, -1),  # Down
    Point(-1, 0),  # Left
]


def load_key_map(key_map):
    grid = {}
    keys = set()
    start = None
    for row, line in enumerate(key_map.splitlines()):
        for col, c in enumerate(line):
            grid[Point(col, row)] = c
            if c == "@":
                print(f"Starting point: {col}, {row}")
                start = Point(col, row)
            elif c.islower():
                keys.add(c)
    return grid, keys, start


# def build_graph(grid, start):
#     # Initialize graph with our starting node
#     graph = {}
#     unexplored = set()
#     unexplored.add(start)
#     graph[start] = []
#     while unexplored:


def retrieve_keys(key_map):
    grid, keys, start = load_key_map(key_map)
    steps = 0
    found_keys = set()
    while found_keys != keys:
        pass
    return 8


key_map = """#########
#b.A.@.a#
#########"""

steps = retrieve_keys(key_map)
assert steps == 8
