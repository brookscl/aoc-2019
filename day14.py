from collections import defaultdict
from math import ceil
from queue import Queue


def create_reaction_graph(reactions):
    reaction_graph = {}
    for reaction in reactions.splitlines():
        source_text, product = reaction.split(" => ")
        product_count, product_name = product.split(" ")
        reaction_graph[product_name] = {}
        reaction_graph[product_name]["count"] = int(product_count)
        reaction_graph[product_name]["sources"] = []
        source_list = source_text.strip().split(", ")
        for source in source_list:
            source_count, source_name = source.split(" ")
            reaction_graph[product_name]["sources"].append(
                (source_name, int(source_count))
            )

    return reaction_graph


def ore_requirement(reaction_graph):
    ore = 0
    supply = defaultdict(int)
    orders = Queue()
    orders.put(("FUEL", 1))
    if isinstance(reaction_graph, str):
        reaction_graph = create_reaction_graph(reaction_graph)

    while not orders.empty():
        order_name, order_count = orders.get()

        if order_name == "ORE":
            ore += order_count
        elif supply[order_name] > order_count:
            supply[order_name] -= order_count
        else:
            order_count -= supply[order_name]

            unit_produced_amount = reaction_graph[order_name]["count"]
            order_multiplier = ceil(order_count / unit_produced_amount)
            total_produced = order_multiplier * unit_produced_amount
            formulas = reaction_graph[order_name]["sources"]
            for formula_name, formula_count in formulas:

                order_size = order_multiplier * formula_count
                orders.put((formula_name, order_size))

            supply[order_name] = total_produced - order_count

    return ore


reactions = "10 ORE => 1 FUEL"

counts = ore_requirement(reactions)
assert counts == 10

reactions = """10 ORE => 3 A
20 A => 1 B
2 B => 1 FUEL"""
counts = ore_requirement(reactions)
assert counts == 140

reactions = """10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL"""


counts = ore_requirement(reactions)
assert counts == 31

reactions = """9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL"""

counts = ore_requirement(reactions)
assert counts == 165

reactions = """157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""

counts = ore_requirement(reactions)
assert counts == 13312

reactions = """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF"""

counts = ore_requirement(reactions)
assert counts == 180697

# Part 1

with open("day14_input.txt") as f:
    reactions = f.readlines()

ore = ore_requirement(" ".join(reactions))
print(ore)
