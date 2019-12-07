from collections import deque


def find_parents(tag, orbit_graph):
    parent_list = []
    current_node = tag
    while current_node != "COM":
        found = False
        for parent, children in orbit_graph.items():
            for child in children:
                if child == current_node:
                    parent_list.append(parent)
                    current_node = parent
                    found = True
                    break
        if not found:
            break
    return parent_list


def total_orbits(orbits):
    orbit_graph = {}
    start = None

    for o in orbits:
        l, r = o.split(")")

        if l in orbit_graph:
            orbit_graph[l].append(r)
        else:
            orbit_graph[l] = [r]

    start = "COM"

    # Walk through graph, breadth first
    explored = []
    queue = deque()
    queue.append(start)
    levels = {}
    levels[start] = 0

    while queue:
        node = queue.pop()
        if node not in explored:
            explored.append(node)
            if node in orbit_graph:
                neighbors = orbit_graph[node]
            else:
                neighbors = []
            for n in neighbors:
                levels[n] = levels[node] + 1
                queue.appendleft(n)

    # Calc santa distance
    you_parents = find_parents("YOU", orbit_graph)
    santa_parents = find_parents("SAN", orbit_graph)
    common_parents = list(set(you_parents) & set(santa_parents))
    closest_parent = -1
    for p in common_parents:
        if levels[p] > closest_parent:
            closest_parent = levels[p]

    print(f"Santa distance: {levels['YOU'] + levels['SAN'] - 2 * closest_parent - 2}")

    return sum(levels.values())


orbits = """COM)B
B)C
C)D
D)YOU
D)E
E)F
B)G
G)H
E)J
J)K
K)SAN"""
orbits = orbits.split("\n")
print(total_orbits(orbits))
assert total_orbits(orbits) == 42


with open("orbits.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
orbits = [x.strip() for x in content]

print(total_orbits(orbits))

# Part 2

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
K)L
K)YOU
I)SAN"""
orbits = orbits.split("\n")
print(total_orbits(orbits))
