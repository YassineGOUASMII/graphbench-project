import networkx as nx


def greedy_independent_domination_number(G):
    dominated = set()
    selected = set()

    nodes = sorted(G.nodes(), key=lambda v: G.degree(v), reverse=True)

    for node in nodes:
        if node in dominated:
            continue

        conflict = False
        for s in selected:
            if G.has_edge(node, s):
                conflict = True
                break

        if not conflict:
            selected.add(node)
            dominated.add(node)
            dominated.update(G.neighbors(node))

    return len(selected)


def greedy_total_domination_number(G):
    """
    Approximation du nombre de domination totale.

    Domination totale :
    chaque sommet doit avoir au moins un voisin dans l'ensemble choisi.
    Contrairement à la domination classique, un sommet ne se domine pas lui-même.
    """
    if G.number_of_nodes() == 0:
        return 0

    selected = set()
    dominated = set()

    nodes = sorted(G.nodes(), key=lambda v: G.degree(v), reverse=True)

    while len(dominated) < G.number_of_nodes():
        best_node = None
        best_gain = -1

        for node in nodes:
            neighbors = set(G.neighbors(node))
            gain = len(neighbors - dominated)

            if gain > best_gain:
                best_gain = gain
                best_node = node

        if best_node is None or best_gain == 0:
            break

        selected.add(best_node)
        dominated.update(G.neighbors(best_node))

    return len(selected)


def compute_invariants(G):
    invariants = {}

    invariants["order"] = G.number_of_nodes()
    invariants["size"] = G.number_of_edges()

    degrees = [d for _, d in G.degree()]

    if degrees:
        invariants["minimum_degree"] = min(degrees)
        invariants["maximum_degree"] = max(degrees)
        invariants["average_degree"] = sum(degrees) / len(degrees)
    else:
        invariants["minimum_degree"] = 0
        invariants["maximum_degree"] = 0
        invariants["average_degree"] = 0

    if G.number_of_nodes() > 0 and nx.is_connected(G):
        invariants["diameter"] = nx.diameter(G)
        invariants["radius"] = nx.radius(G)
        invariants["vertex_connectivity"] = nx.node_connectivity(G)
        invariants["edge_connectivity"] = nx.edge_connectivity(G)
    else:
        invariants["diameter"] = 999
        invariants["radius"] = 999
        invariants["vertex_connectivity"] = 0
        invariants["edge_connectivity"] = 0

    invariants["density"] = nx.density(G)

    invariants["triangle_number"] = sum(nx.triangles(G).values()) // 3

    try:
        cliques = list(nx.find_cliques(G))
        invariants["clique_number"] = max(len(c) for c in cliques) if cliques else 0
    except Exception:
        invariants["clique_number"] = 0

    try:
        independent_set = nx.approximation.maximum_independent_set(G)
        invariants["independence_number"] = len(independent_set)
    except Exception:
        invariants["independence_number"] = 0

    invariants["vertex_cover_number"] = (
        invariants["order"] - invariants["independence_number"]
    )

    try:
        matching = nx.max_weight_matching(G, maxcardinality=True)
        invariants["matching_number"] = len(matching)
    except Exception:
        invariants["matching_number"] = 0

    try:
        dominating_set = nx.approximation.min_weighted_dominating_set(G)
        invariants["domination_number"] = len(dominating_set)
    except Exception:
        invariants["domination_number"] = 0

    try:
        invariants["independent_domination_number"] = greedy_independent_domination_number(G)
    except Exception:
        invariants["independent_domination_number"] = 0

    try:
        invariants["total_domination_number"] = greedy_total_domination_number(G)
    except Exception:
        invariants["total_domination_number"] = 0

    return invariants