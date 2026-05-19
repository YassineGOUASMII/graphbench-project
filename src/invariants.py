import networkx as nx
import numpy as np


def greedy_independent_domination_number(G):
    dominated = set()
    selected = set()

    nodes = sorted(G.nodes(), key=lambda v: G.degree(v), reverse=True)

    for node in nodes:
        if node in dominated:
            continue

        conflict = any(G.has_edge(node, s) for s in selected)

        if not conflict:
            selected.add(node)
            dominated.add(node)
            dominated.update(G.neighbors(node))

    return len(selected)


def greedy_total_domination_number(G):
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


def compute_proximity(G):
    """
    Proximity utilisée dans le benchmark :
    minimum de la closeness centrality.

    closeness(v) = (n - 1) / somme_des_distances_depuis_v
    proximity(G) = min_v closeness(v)
    """
    n = G.number_of_nodes()

    if n <= 1:
        return 0

    if not nx.is_connected(G):
        return 0

    all_lengths = dict(nx.all_pairs_shortest_path_length(G))

    values = []

    for node in G.nodes():
        transmission = sum(all_lengths[node].values())

        if transmission > 0:
            values.append((n - 1) / transmission)

    if not values:
        return 0

    return min(values)


def compute_remoteness(G):
    """
    Remoteness utilisée dans le benchmark :
    maximum de la closeness centrality.

    closeness(v) = (n - 1) / somme_des_distances_depuis_v
    remoteness(G) = max_v closeness(v)
    """
    n = G.number_of_nodes()

    if n <= 1:
        return 0

    if not nx.is_connected(G):
        return 0

    all_lengths = dict(nx.all_pairs_shortest_path_length(G))

    values = []

    for node in G.nodes():
        transmission = sum(all_lengths[node].values())

        if transmission > 0:
            values.append((n - 1) / transmission)

    if not values:
        return 0

    return max(values)


def compute_randic_index(G):
    total = 0
    for u, v in G.edges():
        du = G.degree(u)
        dv = G.degree(v)
        if du > 0 and dv > 0:
            total += 1 / ((du * dv) ** 0.5)
    return total


def compute_harmonic_index(G):
    total = 0
    for u, v in G.edges():
        du = G.degree(u)
        dv = G.degree(v)
        if du + dv > 0:
            total += 2 / (du + dv)
    return total


def compute_first_zagreb_index(G):
    return sum(d ** 2 for _, d in G.degree())


def compute_second_zagreb_index(G):
    return sum(G.degree(u) * G.degree(v) for u, v in G.edges())


def compute_largest_eigenvalue(G):
    if G.number_of_nodes() == 0:
        return 0
    try:
        A = nx.to_numpy_array(G)
        values = np.linalg.eigvals(A)
        return float(max(values.real))
    except Exception:
        return 0


def compute_largest_distance_eigenvalue(G):
    if G.number_of_nodes() == 0:
        return 0
    if not nx.is_connected(G):
        return 0
    try:
        D = nx.floyd_warshall_numpy(G)
        values = np.linalg.eigvals(D)
        return float(max(values.real))
    except Exception:
        return 0


def compute_second_smallest_laplace_eigenvalue(G):
    if G.number_of_nodes() <= 1:
        return 0
    try:
        L = nx.laplacian_matrix(G).toarray()
        values = sorted(np.linalg.eigvals(L).real)
        return float(values[1]) if len(values) > 1 else 0
    except Exception:
        return 0


def compute_invariants(G, required=None):
    if required is None:
        required = []

    required = set(required)

    invariants = {}

    n = G.number_of_nodes()
    m = G.number_of_edges()

    invariants["order"] = n
    invariants["size"] = m

    degrees = [d for _, d in G.degree()]

    if degrees:
        invariants["minimum_degree"] = min(degrees)
        invariants["maximum_degree"] = max(degrees)
        invariants["average_degree"] = sum(degrees) / len(degrees)
    else:
        invariants["minimum_degree"] = 0
        invariants["maximum_degree"] = 0
        invariants["average_degree"] = 0

    invariants["density"] = nx.density(G)

    if (
        "diameter" in required
        or "radius" in required
        or "vertex_connectivity" in required
        or "edge_connectivity" in required
    ):
        if n > 0 and nx.is_connected(G):
            invariants["diameter"] = nx.diameter(G)
            invariants["radius"] = nx.radius(G)
            invariants["vertex_connectivity"] = nx.node_connectivity(G)
            invariants["edge_connectivity"] = nx.edge_connectivity(G)
        else:
            invariants["diameter"] = 999
            invariants["radius"] = 999
            invariants["vertex_connectivity"] = 0
            invariants["edge_connectivity"] = 0
    else:
        invariants["diameter"] = 0
        invariants["radius"] = 0
        invariants["vertex_connectivity"] = 0
        invariants["edge_connectivity"] = 0

    if "proximity" in required:
        invariants["proximity"] = compute_proximity(G)
    else:
        invariants["proximity"] = 0

    if "remoteness" in required:
        invariants["remoteness"] = compute_remoteness(G)
    else:
        invariants["remoteness"] = 0

    if "triangle_number" in required or "clique_number" in required:
        invariants["triangle_number"] = sum(nx.triangles(G).values()) // 3
    else:
        invariants["triangle_number"] = 0

    if "clique_number" in required:
        try:
            cliques = list(nx.find_cliques(G))
            invariants["clique_number"] = max(len(c) for c in cliques) if cliques else 0
        except Exception:
            invariants["clique_number"] = 0
    else:
        invariants["clique_number"] = 0

    if "independence_number" in required or "vertex_cover_number" in required:
        try:
            independent_set = nx.approximation.maximum_independent_set(G)
            invariants["independence_number"] = len(independent_set)
        except Exception:
            invariants["independence_number"] = 0
    else:
        invariants["independence_number"] = 0

    invariants["vertex_cover_number"] = invariants["order"] - invariants["independence_number"]

    if "matching_number" in required:
        try:
            matching = nx.max_weight_matching(G, maxcardinality=True)
            invariants["matching_number"] = len(matching)
        except Exception:
            invariants["matching_number"] = 0
    else:
        invariants["matching_number"] = 0

    if "domination_number" in required:
        try:
            dominating_set = nx.approximation.min_weighted_dominating_set(G)
            invariants["domination_number"] = len(dominating_set)
        except Exception:
            invariants["domination_number"] = 0
    else:
        invariants["domination_number"] = 0

    if "independent_domination_number" in required:
        invariants["independent_domination_number"] = greedy_independent_domination_number(G)
    else:
        invariants["independent_domination_number"] = 0

    if "total_domination_number" in required:
        invariants["total_domination_number"] = greedy_total_domination_number(G)
    else:
        invariants["total_domination_number"] = 0

    if "randic_index" in required:
        invariants["randic_index"] = compute_randic_index(G)
    else:
        invariants["randic_index"] = 0

    if "harmonic_index" in required:
        invariants["harmonic_index"] = compute_harmonic_index(G)
    else:
        invariants["harmonic_index"] = 0

    if "first_zagreb_index" in required:
        invariants["first_zagreb_index"] = compute_first_zagreb_index(G)
    else:
        invariants["first_zagreb_index"] = 0

    if "second_zagreb_index" in required:
        invariants["second_zagreb_index"] = compute_second_zagreb_index(G)
    else:
        invariants["second_zagreb_index"] = 0

    if "largest_eigenvalue" in required:
        invariants["largest_eigenvalue"] = compute_largest_eigenvalue(G)
    else:
        invariants["largest_eigenvalue"] = 0

    if "largest_distance_eigenvalue" in required:
        invariants["largest_distance_eigenvalue"] = compute_largest_distance_eigenvalue(G)
    else:
        invariants["largest_distance_eigenvalue"] = 0

    if "second_smallest_laplace_eigenvalue" in required:
        invariants["second_smallest_laplace_eigenvalue"] = compute_second_smallest_laplace_eigenvalue(G)
    else:
        invariants["second_smallest_laplace_eigenvalue"] = 0

    return invariants