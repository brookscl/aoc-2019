from collections import namedtuple
import re


moons = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""

Point = namedtuple("Point", "x y z")
Velocity = namedtuple("Velocity", "dx dy dz")


def load_moons(moon_text):
    moon_list = []
    for moon in moon_text.splitlines():
        m = re.search("x=(.+?), y=(.+?), z=(.+?)>", moon)
        assert m
        moon_list.append(
            {"pos": Point(int(m[1]), int(m[2]), int(m[3])), "vel": Velocity(0, 0, 0)}
        )
    return moon_list


def adjust_velocity(source, opponent):
    if opponent > source:
        return 1
    if opponent < source:
        return -1
    else:
        return 0


def calculate_velocities(moon_list):
    for moon in moon_list:
        dx, dy, dz = moon["vel"].dx, moon["vel"].dy, moon["vel"].dz
        for opponent in moon_list:
            dx += adjust_velocity(moon["pos"].x, opponent["pos"].x)
            dy += adjust_velocity(moon["pos"].y, opponent["pos"].y)
            dz += adjust_velocity(moon["pos"].z, opponent["pos"].z)
        moon["vel"] = Velocity(dx, dy, dz)
    return moon_list


def move_moons(moon_list):
    for i, moon in enumerate(moon_list):
        moon_list[i]["pos"] = Point(
            moon["pos"].x + moon["vel"].dx,
            moon["pos"].y + moon["vel"].dy,
            moon["pos"].z + moon["vel"].dz,
        )

    return moon_list


# A moon's potential energy is the sum of the absolute values of its x, y,
# and z position coordinates
def potential_energy(moon):
    return abs(moon["pos"].x) + abs(moon["pos"].y) + abs(moon["pos"].z)


# A moon's kinetic energy is the sum of the absolute values of its
# velocity coordinates.
def kinetic_energy(moon):
    return abs(moon["vel"].dx) + abs(moon["vel"].dy) + abs(moon["vel"].dz)


def total_energy(moon):
    return potential_energy(moon) * kinetic_energy(moon)


def total_energy_system(moon_list):
    total = 0
    for moon in moon_list:
        total += total_energy(moon)
    return total


moon_list = load_moons(moons)

assert moon_list[0]["pos"].x == -1
assert moon_list[2]["pos"].z == 8

moon_list = calculate_velocities(moon_list)

assert moon_list[0]["vel"].dx == 3
assert moon_list[2]["vel"].dx == -3
assert moon_list[3]["vel"].dz == 1

moon_list = move_moons(moon_list)
assert moon_list[0]["pos"].x == 2
assert moon_list[2]["pos"].z == 5
assert moon_list[3]["pos"].y == 2

moon_list = load_moons(moons)
for i in range(10):
    moon_list = calculate_velocities(moon_list)
    moon_list = move_moons(moon_list)

assert potential_energy(moon_list[0]) == 6
assert potential_energy(moon_list[2]) == 10
assert kinetic_energy(moon_list[1]) == 5
assert total_energy(moon_list[3]) == 18
assert total_energy_system(moon_list) == 179

# Part 1

moons = """<x=17, y=5, z=1>
<x=-2, y=-8, z=8>
<x=7, y=-6, z=14>
<x=1, y=-10, z=4>"""

moon_list = load_moons(moons)
for i in range(1000):
    moon_list = calculate_velocities(moon_list)
    moon_list = move_moons(moon_list)

print(f"Total energy: {total_energy_system(moon_list)}")
