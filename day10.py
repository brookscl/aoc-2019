from collections import Counter, namedtuple
from math import atan2, degrees, pi
import operator


Point = namedtuple("Point", "x y")
PolarCoord = namedtuple("PolarCoord", "angle distance")


def load_asteroid_map(map):
    asteroids = set()
    for row, line in enumerate(map.splitlines()):
        for col, c in enumerate(line):
            if c == "#":
                asteroids.add(Point(col, row))
    return asteroids


# Ax * (By - Cy) + Bx * (Cy - Ay) + Cx * (Ay - By)
def colinear(a, b, c):
    return (a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y)) == 0


def distance(a, b):
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** (1 / 2.0)


def in_between(a, b, c):
    crossproduct = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)
    if crossproduct != 0:
        return False

    dotproduct = (c.x - a.x) * (b.x - a.x) + (c.y - a.y) * (b.y - a.y)
    if dotproduct < 0:
        return False

    squaredlengthba = (b.x - a.x) * (b.x - a.x) + (b.y - a.y) * (b.y - a.y)
    if dotproduct > squaredlengthba:
        return False

    return True
    # if a.y == b.y:  # Horizontal line
    #     return (a.x < c.x < b.x) or (a.x > c.x > b.x)
    # elif a.x == b.x:  # Vertical line
    #     return (a.y < c.y < b.y) or (a.y > c.y > b.y)
    # else:
    #     return ((a.x < c.x < b.x) and (a.y < c.y < b.y)) or (
    #         (a.x > c.x > b.x) and (a.y > c.y > b.y)
    #     )


# Look for an intervening colinear point
def los(asteroids, a, b):
    # First make sure they are both in the map
    if a not in asteroids or b not in asteroids:
        return False

    # See if there's a blocking, colinear asteroid
    candidate_set = asteroids - {a, b}
    for candidate in candidate_set:
        # if colinear(a, b, candidate):
        if in_between(a, b, candidate):
            return False
            # if distance(a, b) > distance(a, candidate):
            #     return False

    return True


def best_asteroid(asteroids):
    los_counts = Counter()
    # vis_map = {}
    for a in asteroids:
        # vis_map.setdefault(a, [])
        for b in asteroids - {a}:
            if los(asteroids, a, b):
                # vis_map[a].append(b)
                los_counts[a] += 1

    return los_counts.most_common()[0]


map = """.#..#
.....
#####
....#
...##"""

asteroids = load_asteroid_map(map)

assert colinear(Point(0, 6), Point(2, 5), Point(4, 4))
assert colinear(Point(0, 0), Point(3, 1), Point(6, 2))
assert not colinear(Point(0, 0), Point(3, 1), Point(6, 1))

a = Point(1, 0)
b = Point(4, 0)
c = Point(3, 4)
d = Point(2, 2)

assert distance(a, b) == 3
assert los(asteroids, a, b)
assert not los(asteroids, a, c)
assert los(asteroids, a, d)

a = best_asteroid(asteroids)
print(a)
assert a[0] == Point(3, 4)
assert a[1] == 8

map = """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""

a = Point(0, 6)
b = Point(2, 5)
c = Point(4, 4)
asteroids = load_asteroid_map(map)
assert los(asteroids, a, b)
assert not los(asteroids, a, c)

a = best_asteroid(asteroids)
print(a)
assert a[0] == Point(5, 8)
assert a[1] == 33

map = """#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###."""

asteroids = load_asteroid_map(map)
a = best_asteroid(asteroids)
print(a)
assert a[0] == Point(1, 2)
assert a[1] == 35

big_map = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""

# asteroids = load_asteroid_map(map)
# a = best_asteroid(asteroids)
# print(a)
# assert a[0] == Point(11, 13)
# assert a[1] == 210

# Part 1

real_map = """.............#..#.#......##........#..#
.#...##....#........##.#......#......#.
..#.#.#...#...#...##.#...#.............
.....##.................#.....##..#.#.#
......##...#.##......#..#.......#......
......#.....#....#.#..#..##....#.......
...................##.#..#.....#.....#.
#.....#.##.....#...##....#####....#.#..
..#.#..........#..##.......#.#...#....#
...#.#..#...#......#..........###.#....
##..##...#.#.......##....#.#..#...##...
..........#.#....#.#.#......#.....#....
....#.........#..#..##..#.##........#..
........#......###..............#.#....
...##.#...#.#.#......#........#........
......##.#.....#.#.....#..#.....#.#....
..#....#.###..#...##.#..##............#
...##..#...#.##.#.#....#.#.....#...#..#
......#............#.##..#..#....##....
.#.#.......#..#...###...........#.#.##.
........##........#.#...#.#......##....
.#.#........#......#..........#....#...
...............#...#........##..#.#....
.#......#....#.......#..#......#.......
.....#...#.#...#...#..###......#.##....
.#...#..##................##.#.........
..###...#.......#.##.#....#....#....#.#
...#..#.......###.............##.#.....
#..##....###.......##........#..#...#.#
.#......#...#...#.##......#..#.........
#...#.....#......#..##.............#...
...###.........###.###.#.....###.#.#...
#......#......#.#..#....#..#.....##.#..
.##....#.....#...#.##..#.#..##.......#.
..#........#.......##.##....#......#...
##............#....#.#.....#...........
........###.............##...#........#
#.........#.....#..##.#.#.#..#....#....
..............##.#.#.#...........#....."""

asteroids = load_asteroid_map(map)
# a = best_asteroid(asteroids)
# print(a)
# assert a[0] == Point(26, 29)
# assert a[1] == 299

# Part 2


def polar(start, end):
    dist = distance(start, end)
    angle = degrees(atan2(end.x - start.x, start.y - end.y))
    if angle < 0:
        angle += 360.0
    return PolarCoord(angle, dist)


def vaporize(asteroids, base):
    # Collect polar coordinates for all other asteroids
    polars = {}
    for a in asteroids - {base}:
        polars[a] = polar(base, a)
    vapor_ordered = sorted(polars.items(), key=lambda p: (p[1].angle, p[1].distance))
    print(
        f"Polar coordinate list processed, {len(vapor_ordered)} asteroids to destroy."
    )
    return vapor_ordered


def process_canon(canon, vaporize_list):
    vap_seq = []
    i = 0
    while vaporize_list:
        a = vaporize_list[i]
        vap_seq.append(a)
        del vaporize_list[i]
        if len(vaporize_list) == 0:
            break
        i = i % len(vaporize_list)
        if (len(vaporize_list) % 10) == 0:
            print(f"Vaporizing, at {len(vaporize_list)} to prioritize")
        if len(vaporize_list) < 10:
            print(f"  Count-down, at {len(vaporize_list)} to prioritize")

        # If next item in list is colinear, skip it
        if len(vaporize_list) > 1:
            while colinear(canon, a[0], vaporize_list[i][0]):
                i = i + 1
                if i >= len(vaporize_list):
                    i = 0
                    break
    print(f"Canon vaporize list processed, {len(vap_seq)} asteroids to destroy.")
    return vap_seq


map = """.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##"""

a = Point(8, 3)
b = Point(8, 1)
p = polar(a, b)
print(p)
assert p == PolarCoord(0.0, 2.0)
p = polar(b, a)
print(p)
assert p == PolarCoord(180.0, 2.0)
c = Point(9, 0)
p = polar(a, c)
assert 0 < p.angle < 20.0

asteroids = load_asteroid_map(map)
laser_base = best_asteroid(asteroids)[0]
print(laser_base)
assert laser_base == Point(8, 3)
vaporize_todo_list = vaporize(asteroids, laser_base)
vaporize_sequence = process_canon(laser_base, vaporize_todo_list)
first_vaporized = vaporize_sequence[0]
assert first_vaporized[0] == Point(8, 1)
assert [p[0] for p in vaporize_sequence[:5]] == [
    Point(8, 1),
    Point(9, 0),
    Point(9, 1),
    Point(10, 0),
    Point(9, 2),
]

# print("Big map time...")
# asteroids = load_asteroid_map(big_map)
# laser_base = best_asteroid(asteroids)[0]
# print(laser_base)
# assert laser_base == Point(11, 13)
# vaporize_todo_list = vaporize(asteroids, laser_base)
# vaporize_sequence = process_canon(laser_base, vaporize_todo_list)
# first_vaporized = vaporize_sequence[0]
# assert first_vaporized[0] == Point(11, 12)

asteroids = load_asteroid_map(real_map)
laser_base = best_asteroid(asteroids)[0]
print(laser_base)
# assert laser_base == Point(11, 13)
vaporize_todo_list = vaporize(asteroids, laser_base)
vaporize_sequence = process_canon(laser_base, vaporize_todo_list)
print(f"200th asteroid: {vaporize_sequence[199]}")
