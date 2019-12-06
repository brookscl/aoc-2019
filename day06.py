from collections import deque


orbits = ["COM)B", "B)C"]


def total_orbits(orbits):
    orbit_graph = {}
    start = None

    for o in orbits:
        l, r = o.split(')')

        if l in orbit_graph:
            orbit_graph[l].append(r)
        else:
            orbit_graph[l] = [r]

    start = 'COM'

    # Walk through graph, breadth first
    explored = []
    queue = deque()
    queue.append(start)
    levels = {}
    levels[start] = 0
    direct = 0
    indirect = 0

    while queue:
        node = queue.pop()
        if node not in explored:
            explored.append(node)
            if node in orbit_graph:
                neighbors = orbit_graph[node]
            else:
                neighbors = []
            direct += len(neighbors)
            for n in neighbors:
                indirect += 1
                levels[n] = levels[node] + 1
                queue.appendleft(n)
    print(f"Total nodes: {len(levels)}")

    print(f"Other calc: {direct + indirect}")
    return sum(levels.values())


assert total_orbits(orbits) == 3


orbits = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""
orbits = orbits.split("\n")
print(total_orbits(orbits))
assert total_orbits(orbits) == 42

orbits = """COM)A
A)B
A)C
C)D
C)E"""
orbits = orbits.split("\n")
print(total_orbits(orbits))
assert total_orbits(orbits) == 11

with open("orbits.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
orbits = [x.strip() for x in content]

print(total_orbits(orbits))
