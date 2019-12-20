from collections import defaultdict


def create_reaction_graph(reactions):
    reaction_graph = {}
    for reaction in reactions.splitlines():
        source_text, product = reaction.split(" => ")
        product_count, product_name = product.split(" ")
        reaction_graph[product_name] = {}
        reaction_graph[product_name]["dep_count"] = 0
        reaction_graph[product_name]["count"] = int(product_count)
        reaction_graph[product_name]["sources"] = []
        source_list = source_text.split(", ")
        for source in source_list:
            source_count, source_name = source.split(" ")
            reaction_graph[product_name]["sources"].append(
                (source_name, int(source_count))
            )
            if source_name not in reaction_graph:
                reaction_graph[source_name] = {}
                reaction_graph[source_name]["dep_count"] = 0
            reaction_graph[source_name]["dep_count"] += 1

    return reaction_graph


def accumulating(source, g):
    g[source]["dep_count"] -= 1
    return g[source]["dep_count"] > 0


# reactions = "10 ORE => 1 FUEL"
# accumulate_costs("FUEL", 1, counts, reaction_graph)
#
# reactions = """10 ORE => 1 A
#     20 A => 1 B
#     2 B => 1 FUEL"""
def accumulate_costs(product_name, counts, g):
    formula = g[product_name]
    # del g[product_name]
    if "count" not in formula:
        return
    produced_count = formula["count"]
    multiplier = -(-counts[product_name] // produced_count)
    counts[product_name] -= multiplier * produced_count
    if counts[product_name] <= 0:
        del counts[product_name]
    for source, source_count in formula["sources"]:
        # Capture the amount of this source that needs to be produced
        counts[source] += multiplier * source_count
        if not accumulating(source, g):
            accumulate_costs(source, counts, g)


def ore_requirement(reaction_graph):
    counts = defaultdict(int)
    counts["FUEL"] = 1
    if isinstance(reaction_graph, str):
        reaction_graph = create_reaction_graph(reaction_graph)

    accumulate_costs("FUEL", counts, reaction_graph)
    return counts


reactions = "10 ORE => 1 FUEL"

counts = ore_requirement(reactions)
assert counts["ORE"] == 10

reactions = """10 ORE => 1 A
20 A => 1 B
2 B => 1 FUEL"""
counts = ore_requirement(reactions)
assert counts["ORE"] == 400

reactions = """10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL"""


counts = ore_requirement(reactions)
assert counts["ORE"] == 31

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
assert counts["ORE"] == 13312
